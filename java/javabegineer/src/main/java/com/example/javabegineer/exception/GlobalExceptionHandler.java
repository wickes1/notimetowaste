package com.example.javabegineer.exception;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

import com.example.javabegineer.constant.ErrorCode;
import com.example.javabegineer.model.response.GenericResponseModel;

@ControllerAdvice
public class GlobalExceptionHandler {
    private final Logger logger = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    // Catch all unhandled exception
    @ExceptionHandler({ Exception.class })
    public ResponseEntity<GenericResponseModel<Void>> handleException(Exception exception) {
        logger.error(exception.getMessage(), exception);

        return ResponseEntity
                .status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(new GenericResponseModel<>(ErrorCode.UNEXPECTED_SYSTEM_ERROR));
    }
}
