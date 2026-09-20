package com.krismih.backend.summary.entity;

import com.krismih.backend.auth.entity.User;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

@Entity
@Table(name = "summaries")
@Getter
@Setter
public class Summary {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private long id;

    @Column(name = "input")
    private String input;
    @Column(name = "summary")
    private String summary;

    @ManyToOne
    @JoinColumn(name = "associated_user")
    private User associatedUser;
}
