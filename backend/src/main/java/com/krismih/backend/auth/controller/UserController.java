package com.krismih.backend.auth.controller;

import com.krismih.backend.auth.dto.request.LoginRequest;
import com.krismih.backend.auth.dto.request.LogoutRequest;
import com.krismih.backend.auth.dto.request.RefreshTokenRequest;
import com.krismih.backend.auth.dto.request.RegisterRequest;
import com.krismih.backend.auth.dto.response.AuthResponse;
import com.krismih.backend.auth.dto.response.UserDetailsResponse;
import com.krismih.backend.auth.entity.User;
import com.krismih.backend.auth.repository.UserRepository;
import com.krismih.backend.auth.service.UserService;
import com.krismih.backend.exception.custom.ResourceNotFoundException;
import com.krismih.backend.summary.dto.response.SummariesResponse;
import com.krismih.backend.summary.repository.SummaryRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@RestController
@RequestMapping("/api/v1/auth")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @PostMapping("/register")
    public ResponseEntity<Void> register(@Valid @RequestBody RegisterRequest request) {
        userService.registerUser(request);
        return ResponseEntity.status(HttpStatus.CREATED).build();
    }

    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(@Valid @RequestBody LoginRequest request) {
        AuthResponse response = userService.loginUser(request);
        return ResponseEntity.status(HttpStatus.OK).body(response);
    }

    @PostMapping("/refresh")
    public ResponseEntity<AuthResponse> refresh(@RequestBody RefreshTokenRequest request) {
        AuthResponse response = userService.refresh(request.refreshToken());
        return ResponseEntity.status(HttpStatus.OK).body(response);
    }

    @PostMapping("/logout")
    public ResponseEntity<Void> logout(@RequestBody LogoutRequest request) {
        userService.logoutUser(request.refreshToken());
        return ResponseEntity.status(HttpStatus.NO_CONTENT).build();
    }

    @GetMapping("/me")
    public ResponseEntity<UserDetailsResponse> getCurrentUser() {
        return ResponseEntity.status(HttpStatus.OK).body(userService.getCurrentUser());
    }

    @GetMapping("/summaries")
    public ResponseEntity<SummariesResponse> getSummariesController() {
        return ResponseEntity.status(HttpStatus.OK).body(this.userService.getSummaries());
    }
}
