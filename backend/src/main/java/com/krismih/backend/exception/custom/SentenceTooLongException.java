package com.krismih.backend.exception.custom;

public class SentenceTooLongException extends RuntimeException {
    public SentenceTooLongException(String message) {
        super(message);
    }
}
