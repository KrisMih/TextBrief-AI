package com.krismih.backend.exception.dto;

import java.time.Instant;

public record GeneralErrorResponse(
        int status,
        String error,
        String message,
        Instant timestamp,
        String path
) {}
