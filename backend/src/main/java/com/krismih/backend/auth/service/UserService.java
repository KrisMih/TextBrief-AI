package com.krismih.backend.auth.service;

import com.krismih.backend.auth.dto.request.LoginRequest;
import com.krismih.backend.auth.dto.request.RegisterRequest;
import com.krismih.backend.auth.dto.response.AuthResponse;
import com.krismih.backend.auth.dto.response.UserDetailsResponse;
import com.krismih.backend.auth.entity.RefreshToken;
import com.krismih.backend.auth.entity.User;
import com.krismih.backend.auth.repository.UserRepository;
import com.krismih.backend.exception.custom.ResourceNotFoundException;
import com.krismih.backend.security.JwtUtil;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtUtil jwtUtil;
    private final RefreshTokenService refreshTokenService;

    public UserService(UserRepository userRepository,  PasswordEncoder passwordEncoder,  JwtUtil jwtUtil,  RefreshTokenService refreshTokenService) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtUtil = jwtUtil;
        this.refreshTokenService = refreshTokenService;
    }

    public void registerUser(RegisterRequest request) {

        if (userRepository.findByUsername(request.username()).isPresent()) {
            throw new IllegalStateException("Username already exists.");
        }

        String hashedPassword = passwordEncoder.encode(request.password());

        User user = new User();
        user.setUsername(request.username());
        user.setPassword(hashedPassword);

        userRepository.save(user);
    }

    public AuthResponse loginUser(LoginRequest request) {

        User user = userRepository.findByUsername(request.username())
                .orElseThrow(() -> new ResourceNotFoundException("Invalid username."));

        if(!passwordEncoder.matches(request.password(), user.getPassword())) {
            throw new IllegalStateException("Invalid password.");
        }

        String accessToken = jwtUtil.generateToken(user.getUsername());

        RefreshToken refreshToken = refreshTokenService.create(user);

        return new AuthResponse(accessToken, refreshToken.getToken());
    }

    public AuthResponse refresh(String refreshToken) {
        String username = refreshTokenService.validate(refreshToken);

        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        String newAccessToken = jwtUtil.generateToken(user.getUsername());
        RefreshToken newRefreshToken = refreshTokenService.create(user);

        return new AuthResponse(newAccessToken, newRefreshToken.getToken());
    }

    public void logoutUser(String refreshToken) {
        refreshTokenService.deleteToken(refreshToken);
    }


    public UserDetailsResponse getCurrentUser() {

        String username = SecurityContextHolder.getContext().getAuthentication().getName();

        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        return new UserDetailsResponse(user.getId(), user.getUsername());
    }
}