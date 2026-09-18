package com.krismih.backend.auth.dto.response;

import com.krismih.backend.auth.entity.User;

public record UserDetailsResponse(
        Long id,
        String username
) {

    public static  UserDetailsResponse from(User u) {
        return new UserDetailsResponse(
                u.getId(),
                u.getUsername()
        );
    }
}
