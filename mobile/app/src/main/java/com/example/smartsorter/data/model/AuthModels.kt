package com.example.smartsorter.data.model

import com.google.gson.annotations.SerializedName

data class AuthData(
    @SerializedName("access_token") val accessToken: String,
    @SerializedName("token_type") val tokenType: String
)

data class UserCreateRequest(
    @SerializedName("username") val username: String,
    @SerializedName("role") val role: String,
    @SerializedName("password") val password: String
)

data class UserResponse(
    @SerializedName("id") val id: Int,
    @SerializedName("username") val username: String,
    @SerializedName("role") val role: String
)