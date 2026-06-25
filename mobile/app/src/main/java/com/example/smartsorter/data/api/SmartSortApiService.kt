package com.example.smartsorter.data.api

import com.example.smartsorter.data.model.*
import retrofit2.Response
import retrofit2.http.*

interface SmartSortApiService {

    @POST("users/")
    suspend fun registerUser(
        @Body request: UserCreateRequest
    ): Response<UserResponse>

    @POST("token")
    @FormUrlEncoded
    suspend fun loginDriver(
        @Field("username") username: String,
        @Field("password") password: String
    ): Response<AuthData>

    // Containers
    @GET("containers/")
    suspend fun getContainers(
        @Header("Authorization") bearerToken: String
    ): Response<List<ContainerResponse>>

    @GET("containers/{id}")
    suspend fun getContainerById(
        @Header("Authorization") bearerToken: String,
        @Path("id") containerId: Int
    ): Response<ContainerResponse>

    @PATCH("containers/{id}/fill-level")
    suspend fun updateContainerFillLevel(
        @Header("Authorization") bearerToken: String,
        @Path("id") containerId: Int,
        @Body request: ContainerFillLevelUpdate
    ): Response<ContainerResponse>

    // Routes
    @GET("routes/")
    suspend fun getRoutes(
        @Header("Authorization") bearerToken: String
    ): Response<List<RouteResponse>>

    @GET("routes/{id}")
    suspend fun getRouteById(
        @Header("Authorization") bearerToken: String,
        @Path("id") routeId: Int
    ): Response<RouteResponse>

    // Alerts (for driver to report issues)
    @POST("alerts/")
    suspend fun createAlert(
        @Header("Authorization") bearerToken: String,
        @Body alert: AlertCreateRequest
    ): Response<Unit>
}