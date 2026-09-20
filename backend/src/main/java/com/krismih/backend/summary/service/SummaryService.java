package com.krismih.backend.summary.service;

import com.krismih.backend.auth.entity.User;
import com.krismih.backend.auth.repository.UserRepository;
import com.krismih.backend.exception.custom.ResourceNotFoundException;
import com.krismih.backend.exception.custom.SentenceTooLongException;
import com.krismih.backend.summary.dto.request.SummaryRequest;
import com.krismih.backend.summary.dto.response.AiResponse;
import com.krismih.backend.summary.dto.response.SummaryResponse;
import com.krismih.backend.summary.entity.Summary;
import com.krismih.backend.summary.repository.SummaryRepository;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.client.JdkClientHttpRequestFactory;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestClientResponseException;
import org.springframework.web.server.ResponseStatusException;

import java.net.http.HttpClient;
import java.util.Map;

@Service
public class SummaryService {

    private final UserRepository userRepository;
    private final SummaryRepository summaryRepository;
    private final RestClient aiClient;

    public SummaryService(
            UserRepository userRepository,
            SummaryRepository summaryRepository,
            @Value("${textbrief.ai.base-url}") String aiBaseUrl
    ) {
        this.userRepository = userRepository;
        this.summaryRepository = summaryRepository;

        HttpClient httpClient = HttpClient.newBuilder()
                .version(HttpClient.Version.HTTP_1_1)
                .build();

        this.aiClient = RestClient.builder()
                .baseUrl(aiBaseUrl)
                .requestFactory(new JdkClientHttpRequestFactory(httpClient))
                .build();
    }

    public SummaryResponse createSummary(SummaryRequest request) {
        if (request == null || request.text() == null || request.text().isBlank()) {
            throw new ResponseStatusException(
                    HttpStatus.BAD_REQUEST,
                    "Text cannot be empty."
            );
        }

        String text = request.text();

        if (text.length() > 20_000) {
            throw new SentenceTooLongException("Text is too long.");
        }

        Authentication authentication = SecurityContextHolder
                .getContext()
                .getAuthentication();

        if (authentication == null
                || !authentication.isAuthenticated()
                || "anonymousUser".equals(authentication.getPrincipal())) {
            throw new ResponseStatusException(
                    HttpStatus.UNAUTHORIZED,
                    "Authentication is required."
            );
        }

        User currentUser = userRepository
                .findByUsername(authentication.getName())
                .orElseThrow(() ->
                        new ResourceNotFoundException("User not found.")
                );

        String generatedSummary = generateSummary(text);

        Summary summary = new Summary();
        summary.setInput(text);
        summary.setSummary(generatedSummary);
        summary.setAssociatedUser(currentUser);

        Summary savedSummary = summaryRepository.save(summary);

        return new SummaryResponse(
                savedSummary.getId(),
                savedSummary.getSummary()
        );
    }

    private String generateSummary(String text) {
        try {
            AiResponse response = aiClient.post()
                    .uri("/summarize")
                    .contentType(MediaType.APPLICATION_JSON)
                    .body(Map.of("text", text, "topK", 2))
                    .retrieve()
                    .body(AiResponse.class);

            if (response == null
                    || response.summary() == null
                    || response.summary().isBlank()) {
                throw new ResponseStatusException(
                        HttpStatus.BAD_GATEWAY,
                        "Invalid response from the AI service."
                );
            }

            return response.summary();

        } catch (ResourceAccessException exception) {
            throw new ResponseStatusException(
                    HttpStatus.SERVICE_UNAVAILABLE,
                    "The AI service is unavailable.",
                    exception
            );

        } catch (RestClientResponseException exception) {
            if (exception.getStatusCode().value() == 422) {
                throw new ResponseStatusException(
                        HttpStatus.UNPROCESSABLE_CONTENT,
                        "The AI service rejected the text.",
                        exception
                );
            }

            throw new ResponseStatusException(
                    HttpStatus.BAD_GATEWAY,
                    "The AI service failed.",
                    exception
            );
        }
    }
}