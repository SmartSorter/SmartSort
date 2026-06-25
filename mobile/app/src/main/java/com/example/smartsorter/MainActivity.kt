package com.example.smartsorter

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.foundation.layout.padding
import com.example.smartsorter.data.api.SmartSortApiService
import com.example.smartsorter.ui.screen.DriverDashboardScreen
import com.example.smartsorter.ui.screen.LoginScreen
import com.example.smartsorter.ui.screen.RoutesScreen
import com.example.smartsorter.ui.screen.AlertsScreen
import com.example.smartsorter.ui.viewmodel.DriverRouteViewModel
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val retrofit = Retrofit.Builder()
            .baseUrl("https://smartsort-h0co.onrender.com/")
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        val apiService = retrofit.create(SmartSortApiService::class.java)
        val viewModel = DriverRouteViewModel(apiService)

        setContent {
            MaterialTheme {
                val isAuthorized by viewModel.isAuthorized.collectAsState()
                var currentScreen by remember { mutableStateOf("dashboard") }

                if (!isAuthorized) {
                    LoginScreen(viewModel = viewModel)
                } else {
                    Scaffold(
                        bottomBar = {
                            NavigationBar {
                                NavigationBarItem(
                                    icon = { Text("🗑️") },
                                    label = { Text("Баки") },
                                    selected = currentScreen == "dashboard",
                                    onClick = { currentScreen = "dashboard" }
                                )
                                NavigationBarItem(
                                    icon = { Text("🗺️") },
                                    label = { Text("Маршрути") },
                                    selected = currentScreen == "routes",
                                    onClick = { currentScreen = "routes" }
                                )
                                NavigationBarItem(
                                    icon = { Text("⚠️") },
                                    label = { Text("Звіти") },
                                    selected = currentScreen == "alerts",
                                    onClick = { currentScreen = "alerts" }
                                )
                            }
                        }
                    ) { innerPadding ->
                        androidx.compose.foundation.layout.Box(modifier = Modifier.padding(innerPadding)) {
                            when (currentScreen) {
                                "dashboard" -> DriverDashboardScreen(viewModel = viewModel)
                                "routes" -> RoutesScreen(viewModel = viewModel)
                                "alerts" -> AlertsScreen(viewModel = viewModel)
                            }
                        }
                    }
                }
            }
        }
    }
}