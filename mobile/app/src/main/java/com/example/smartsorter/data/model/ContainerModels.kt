package com.example.smartsorter.data.model

import com.google.gson.annotations.SerializedName

data class ContainerResponse(
    @SerializedName("id") val id: Int,
    @SerializedName("device_id") val deviceId: Int,
    @SerializedName("waste_type_id") val wasteTypeId: Int,
    @SerializedName("fill_level") val fillLevel: Int
)

data class ContainerFillLevelUpdate(
    @SerializedName("fill_level") val fillLevel: Int
)

data class RouteResponse(
    @SerializedName("id") val id: Int,
    @SerializedName("description") val description: String?,
    @SerializedName("created_at") val createdAt: String
)

data class AlertCreateRequest(
    @SerializedName("message") val message: String,
    @SerializedName("container_id") val containerId: Int?
)