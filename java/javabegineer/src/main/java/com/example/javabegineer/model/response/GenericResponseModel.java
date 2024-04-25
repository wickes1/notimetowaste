package com.example.javabegineer.model.response;

import com.example.javabegineer.constant.ResponseStatus;

public class GenericResponseModel<T> {
    private ResponseStatus status;
    private T body;
    private String errorCode;
    private String errorMsg;

    public GenericResponseModel() {
    }

    public GenericResponseModel(ResponseStatus status) {
        this.status = status;
    }

    public GenericResponseModel(ResponseStatus status, T body) {
        this.status = status;
        this.body = body;
    }

    public GenericResponseModel(String errorCode) {
        this.status = ResponseStatus.FAIL;
        this.errorCode = errorCode;
    }

    public GenericResponseModel(String errorCode, String errorMsg) {
        this.status = ResponseStatus.FAIL;
        this.errorCode = errorCode;
        this.errorMsg = errorMsg;
    }

    public ResponseStatus getStatus() {
        return status;
    }

    public void setStatus(ResponseStatus status) {
        this.status = status;
    }

    public T getBody() {
        return body;
    }

    public void setBody(T body) {
        this.body = body;
    }

    public String getErrorCode() {
        return errorCode;
    }

    public void setErrorCode(String errorCode) {
        this.errorCode = errorCode;
    }

    public String getErrorMsg() {
        return errorMsg;
    }

    public void setErrorMsg(String errorMsg) {
        this.errorMsg = errorMsg;
    }
}
