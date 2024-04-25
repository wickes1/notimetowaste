package com.example.javabegineer.entity;

import java.util.Date;

import com.example.javabegineer.model.request.AddStudentRequestModel;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Table;
import jakarta.persistence.Temporal;
import jakarta.persistence.TemporalType;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "student")
@Getter
@Setter
@NoArgsConstructor
public class StudentEntity extends BaseEntity {

    @Column(name = "first_name")
    private String firstName;

    @Column(name = "last_name")
    private String lastName;

    @Temporal(TemporalType.DATE)
    @Column(name = "dob")
    private Date dob;

    @Column(name = "email")
    private String email;

    public StudentEntity(AddStudentRequestModel model) {
        this.firstName = model.getFirstName();
        this.lastName = model.getFamilyName();
        this.dob = model.getDob();
        this.email = model.getEmail();
    }
}
