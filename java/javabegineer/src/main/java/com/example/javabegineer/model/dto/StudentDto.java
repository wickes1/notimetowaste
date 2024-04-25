package com.example.javabegineer.model.dto;

import java.util.Date;

import com.example.javabegineer.entity.StudentEntity;

import lombok.Getter;
import lombok.Setter;

// Dto class for student, used for return targeted data to frontend
@Getter
@Setter
public class StudentDto {
    private Long id;
    private String firstName;
    private String familyName;
    private Date dob;
    private String email;

    public StudentDto(StudentEntity entity) {
        this.id = entity.getId();
        this.firstName = entity.getFirstName();
        this.familyName = entity.getLastName();
        this.dob = entity.getDob();
        this.email = entity.getEmail();
    }

}
