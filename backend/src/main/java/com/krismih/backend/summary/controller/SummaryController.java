package com.krismih.backend.summary.controller;

import com.krismih.backend.summary.dto.request.SummaryRequest;
import com.krismih.backend.summary.dto.response.SummaryResponse;
import com.krismih.backend.summary.service.SummaryService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/summaries")
public class SummaryController {

    private final SummaryService summaryService;

    public SummaryController(SummaryService summaryService) {
        this.summaryService = summaryService;
    }

    @PostMapping("/create")
    public ResponseEntity<SummaryResponse> createSummary(
            @Valid @RequestBody SummaryRequest request
    ) {
        SummaryResponse response = summaryService.createSummary(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }
}