package com.krismih.backend.summary.dto.request;

import jakarta.validation.constraints.NotBlank;

public record SummaryRequest(
        @NotBlank(message = "Text cannot be empty.")
        String text
) {}
