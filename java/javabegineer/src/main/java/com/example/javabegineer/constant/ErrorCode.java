package com.example.javabegineer.constant;

// class to hold all error codes returned to front-end
public class ErrorCode {
    // 1. Validation Errors -> Error thrown by validation for requestBody
    // - Student Fields Error Code
    public final static String INVALID_STUDENT_ID = "INVALID_STUDENT_ID";
    public final static String INVALID_STUDENT_FIRSTNAME = "INVALID_STUDENT_FIRSTNAME";
    public final static String INVALID_STUDENT_FAMILYNAME = "INVALID_STUDENT_FAMILYNAME";
    public final static String INVALID_STUDENT_DOB = "INVALID_STUDENT_DOB";
    public final static String INVALID_STUDENT_EMAIL = "INVALID_STUDENT_EMAIL";

    // - Course Fields Error Code
    public final static String INVALID_COURSE_ID = "INVALID_COURSE_ID";
    public final static String INVALID_COURSE_NAME = "INVALID_COURSE_NAME";

    // - Result Fields Error Code
    public final static String INVALID_RESULT_SCORE = "INVALID_RESULT_SCORE";

    // 2. Data Errors -> Error thrown when saving to database, which is expected
    // behavior (e.g. violation of Result unique index)
    // - Result Data Error Code
    public final static String DATA_RESULT_EXISTS = "DATA_RESULT_EXISTS";

    // 3. System Errors
    public final static String UNEXPECTED_SYSTEM_ERROR = "UNEXPECTED_SYSTEM_ERROR";
}
