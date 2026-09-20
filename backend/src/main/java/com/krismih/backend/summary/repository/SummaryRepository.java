package com.krismih.backend.summary.repository;

import com.krismih.backend.auth.entity.User;
import com.krismih.backend.summary.entity.Summary;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Collection;
import java.util.List;

@Repository
public interface SummaryRepository extends JpaRepository<Summary, Long> {
    List<Summary> findAllByAssociatedUserOrderByIdDesc(User currentUser);
}
