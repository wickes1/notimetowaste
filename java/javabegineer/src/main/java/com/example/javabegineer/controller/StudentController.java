package com.example.javabegineer.controller;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.javabegineer.constant.ResponseStatus;
import com.example.javabegineer.entity.StudentEntity;
import com.example.javabegineer.model.dto.StudentDto;
import com.example.javabegineer.model.request.AddStudentRequestModel;
import com.example.javabegineer.model.response.GenericResponseModel;
import com.example.javabegineer.service.StudentService;

import jakarta.validation.Valid;

@RestController
@RequestMapping("/student")
public class StudentController {
    private final StudentService studentService;

    public StudentController(StudentService studentService) {
        this.studentService = studentService;
    }

    @PostMapping
    public GenericResponseModel<StudentDto> addStudent(@Valid @RequestBody AddStudentRequestModel model)
            throws Exception {
        StudentEntity savedEntity = studentService.addStudent(model);
        return new GenericResponseModel<>(ResponseStatus.SUCCESS, new StudentDto(savedEntity));
    }

}
