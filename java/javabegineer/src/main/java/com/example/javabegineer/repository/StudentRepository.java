package com.example.javabegineer.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.javabegineer.entity.StudentEntity;

public interface StudentRepository extends JpaRepository<StudentEntity, Long> {

}
