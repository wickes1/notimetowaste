package com.example.javabegineer.service;

import org.springframework.stereotype.Service;

import com.example.javabegineer.entity.StudentEntity;
import com.example.javabegineer.model.request.AddStudentRequestModel;
import com.example.javabegineer.repository.StudentRepository;

import jakarta.transaction.Transactional;

@Service
public class StudentService {

    private final StudentRepository repository;

    public StudentService(StudentRepository repository) {
        this.repository = repository;
    }

    @Transactional
    public StudentEntity addStudent(AddStudentRequestModel model) {
        StudentEntity entity = new StudentEntity(model);
        return repository.save(entity);
    }
}
