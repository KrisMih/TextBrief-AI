package com.krismih.backend.exception;

import com.krismih.backend.exception.custom.AccessDeniedException;
import com.krismih.backend.exception.custom.DuplicateResourceException;
import com.krismih.backend.exception.custom.ResourceNotFoundException;
import com.krismih.backend.exception.custom.SentenceTooLongException;
import com.krismih.backend.exception.dto.GeneralErrorResponse;
import com.krismih.backend.exception.dto.ValidationErrorResponse;
import jakarta.servlet.http.HttpServletRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.security.core.AuthenticationException;

import java.time.Instant;
import java.util.Map;
import java.util.stream.Collectors;

@RestControllerAdvice
public class GlobalExceptionHandler {
    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    private ResponseEntity<GeneralErrorResponse> buildError(HttpStatus status, String message, String path) {
        GeneralErrorResponse response = new GeneralErrorResponse(
                status.value(),
                status.getReasonPhrase(),
                message,
                Instant.now(),
                path
        );
        return ResponseEntity.status(status).body(response);
    }



    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<GeneralErrorResponse> handleNotFound(ResourceNotFoundException ex, HttpServletRequest req) {
        log.warn("Resource not found: {}", ex.getMessage());
        return buildError(HttpStatus.NOT_FOUND, ex.getMessage(), req.getRequestURI());
    }

    @ExceptionHandler(DuplicateResourceException.class)
    public ResponseEntity<GeneralErrorResponse> handleDuplicate(DuplicateResourceException ex, HttpServletRequest req) {
        log.warn("Duplicate resource: {}", ex.getMessage());
        return buildError(HttpStatus.CONFLICT, ex.getMessage(), req.getRequestURI());
    }

    @ExceptionHandler(RuntimeException.class)
    public ResponseEntity<GeneralErrorResponse> handleRuntime(RuntimeException ex, HttpServletRequest req) {
        log.error("Runtime exception: {}", ex.getMessage(), ex);
        return buildError(HttpStatus.INTERNAL_SERVER_ERROR, ex.getMessage(), req.getRequestURI());
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<GeneralErrorResponse> handleGeneric(Exception ex, HttpServletRequest req) {
        log.error("Unexpected exception: {}", ex.getMessage(), ex);
        return buildError(HttpStatus.INTERNAL_SERVER_ERROR, "Unexpected server error", req.getRequestURI());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ValidationErrorResponse> handleValidation(MethodArgumentNotValidException ex, HttpServletRequest req) {

        Map<String, String> fieldErrors = ex.getBindingResult()
                .getFieldErrors()
                .stream()
                .collect(Collectors.toMap(
                        err -> err.getField(),
                        err -> err.getDefaultMessage(),
                        (a, b) -> b
                ));

        ValidationErrorResponse response = new ValidationErrorResponse(
                HttpStatus.BAD_REQUEST.value(),
                HttpStatus.BAD_REQUEST.getReasonPhrase(),
                "Validation failed",
                fieldErrors,
                Instant.now(),
                req.getRequestURI()
        );

        log.warn("Validation failed: {}", fieldErrors);

        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(response);
    }

    @ExceptionHandler(org.springframework.security.access.AccessDeniedException.class)
    public ResponseEntity<GeneralErrorResponse> handleSecurityAccessDenied(
            org.springframework.security.access.AccessDeniedException ex, HttpServletRequest req) {
        log.warn("Insufficient permissions: {}", ex.getMessage());
        return buildError(HttpStatus.FORBIDDEN, "You do not have permission to perform this action.", req.getRequestURI());
    }


    @ExceptionHandler(AccessDeniedException.class)
    public ResponseEntity<GeneralErrorResponse> handleAccessDenied(AccessDeniedException ex, HttpServletRequest req) {
        log.warn("Access denied: {}", ex.getMessage());
        return buildError(HttpStatus.FORBIDDEN, ex.getMessage(), req.getRequestURI());
    }


    @ExceptionHandler(SentenceTooLongException.class)
    public ResponseEntity<GeneralErrorResponse> handleMaxSizeReached(SentenceTooLongException ex, HttpServletRequest req) {
        log.warn("Max sentence length reached: {}", ex.getMessage());
        return buildError(HttpStatus.FORBIDDEN, ex.getMessage(), req.getRequestURI());
    }
}
