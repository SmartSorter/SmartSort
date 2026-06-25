package com.example.smartsorter.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.smartsorter.data.api.SmartSortApiService
import com.example.smartsorter.data.model.ContainerFillLevelUpdate
import com.example.smartsorter.data.model.ContainerResponse
import com.example.smartsorter.data.model.RouteResponse
import com.example.smartsorter.data.model.AlertCreateRequest
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

sealed class SmartSortUiState {
    object Idle : SmartSortUiState()
    object Loading : SmartSortUiState()
    data class Success(val containers: List<ContainerResponse>) : SmartSortUiState()
    data class Error(val message: String) : SmartSortUiState()
}

class DriverRouteViewModel(private val apiService: SmartSortApiService) : ViewModel() {

    private val _uiState = MutableStateFlow<SmartSortUiState>(SmartSortUiState.Idle)
    val uiState: StateFlow<SmartSortUiState> = _uiState.asStateFlow()

    private val _isAuthorized = MutableStateFlow(false)
    val isAuthorized: StateFlow<Boolean> = _isAuthorized.asStateFlow()

    private val _routesState = MutableStateFlow<List<RouteResponse>>(emptyList())
    val routesState: StateFlow<List<RouteResponse>> = _routesState.asStateFlow()

    private val _alertStatus = MutableStateFlow<String>("")
    val alertStatus: StateFlow<String> = _alertStatus.asStateFlow()

    private var sessionToken: String = ""

    fun login(username: String, password: String) {
        viewModelScope.launch {
            _uiState.value = SmartSortUiState.Loading
            try {
                val response = apiService.loginDriver(username, password)
                if (response.isSuccessful && response.body() != null) {
                    val authData = response.body()!!
                    sessionToken = "${authData.tokenType} ${authData.accessToken}"
                    _isAuthorized.value = true
                    loadAssignedContainers()
                } else {
                    _uiState.value = SmartSortUiState.Error("Неправильний логін або пароль")
                }
            } catch (e: Exception) {
                _uiState.value = SmartSortUiState.Error("Помилка мережі")
            }
        }
    }

    fun register(username: String, password: String) {
        viewModelScope.launch {
            _uiState.value = SmartSortUiState.Loading
            try {
                val request = com.example.smartsorter.data.model.UserCreateRequest(username, "driver", password)
                val response = apiService.registerUser(request)
                if (response.isSuccessful) {
                    // Automatically log in after registration
                    login(username, password)
                } else {
                    _uiState.value = SmartSortUiState.Error("Не вдалося зареєструватися. Можливо користувач вже існує.")
                }
            } catch (e: Exception) {
                _uiState.value = SmartSortUiState.Error("Помилка мережі")
            }
        }
    }

    fun loadAssignedContainers() {
        viewModelScope.launch {
            _uiState.value = SmartSortUiState.Loading
            try {
                val response = apiService.getContainers(sessionToken)
                if (response.isSuccessful && response.body() != null) {
                    _uiState.value = SmartSortUiState.Success(response.body()!!)
                } else {
                    _uiState.value = SmartSortUiState.Error("Не вдалося завантажити маршрут")
                }
            } catch (e: Exception) {
                _uiState.value = SmartSortUiState.Error("Помилка зчитування даних")
            }
        }
    }

    fun clearContainerTask(containerId: Int) {
        viewModelScope.launch {
            try {
                val response = apiService.updateContainerFillLevel(
                    bearerToken = sessionToken,
                    containerId = containerId,
                    request = ContainerFillLevelUpdate(0)
                )
                if (response.isSuccessful) {
                    loadAssignedContainers()
                }
            } catch (e: Exception) {
            }
        }
    }

    fun loadRoutes() {
        viewModelScope.launch {
            try {
                val response = apiService.getRoutes(sessionToken)
                if (response.isSuccessful && response.body() != null) {
                    _routesState.value = response.body()!!
                }
            } catch (e: Exception) {
            }
        }
    }

    fun submitAlert(message: String, containerId: Int?) {
        viewModelScope.launch {
            _alertStatus.value = "Відправка..."
            try {
                val response = apiService.createAlert(sessionToken, AlertCreateRequest(message, containerId))
                if (response.isSuccessful) {
                    _alertStatus.value = "Звіт відправлено успішно!"
                } else {
                    _alertStatus.value = "Помилка відправки."
                }
            } catch (e: Exception) {
                _alertStatus.value = "Помилка мережі."
            }
        }
    }

    fun resetAlertStatus() {
        _alertStatus.value = ""
    }
}