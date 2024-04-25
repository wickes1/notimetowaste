package com.example.javabegineer.model.request;

import java.util.Date;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class AddStudentRequestModel {
    @NotBlank
    private String firstName;

    @NotBlank
    private String familyName;

    @NotNull
    private Date dob;

    // Check for email, should not be blank and with defined format
    // using @Email hibernate validator to do the primary check of email format
    // as well as an addition regex ".+@.+\\..+" for preventing email without top
    // level domain (i.e. @Email will permit email like w@goo)
    @NotBlank
    @Email(regexp = ".+@.+\\..+")
    private String email;

    public AddStudentRequestModel(String firstName, String familyName, Date dob, String email) {
        this.firstName = firstName;
        this.familyName = familyName;
        this.dob = dob;
        this.email = email;
    }
}
