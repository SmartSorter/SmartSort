package com.example.smartsorter.ui.screen

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.example.smartsorter.data.model.ContainerResponse
import com.example.smartsorter.ui.viewmodel.DriverRouteViewModel
import com.example.smartsorter.ui.viewmodel.SmartSortUiState

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DriverDashboardScreen(viewModel: DriverRouteViewModel) {
    val uiState by viewModel.uiState.collectAsState()

    androidx.compose.runtime.LaunchedEffect(Unit) {
        viewModel.loadAssignedContainers()
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Маршрут Водія", color = Color.White) },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.primary)
            )
        }
    ) { paddingValues ->
        Box(modifier = Modifier.fillMaxSize().padding(paddingValues).background(MaterialTheme.colorScheme.background)) {
            when (uiState) {
                is SmartSortUiState.Loading -> CircularProgressIndicator(modifier = Modifier.align(Alignment.Center))
                is SmartSortUiState.Success -> {
                    val list = (uiState as SmartSortUiState.Success).containers
                    if (list.isEmpty()) {
                        Text("Маршрут порожній!", modifier = Modifier.align(Alignment.Center))
                    } else {
                        LazyColumn(modifier = Modifier.fillMaxSize().padding(12.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                            items(list) { container ->
                                WasteContainerCard(container = container, onClean = { viewModel.clearContainerTask(container.id) })
                            }
                        }
                    }
                }
                is SmartSortUiState.Error -> Text((uiState as SmartSortUiState.Error).message, color = MaterialTheme.colorScheme.error, modifier = Modifier.align(Alignment.Center))
                else -> {}
            }
        }
    }
}

@Composable
fun WasteContainerCard(container: ContainerResponse, onClean: () -> Unit) {
    val colorIndicator = when {
        container.fillLevel >= 90 -> Color(0xFFC62828) // CRITICAL
        container.fillLevel >= 70 -> Color(0xFFEF6C00) // WARNING
        else -> Color(0xFF2E7D32)
    }

    Card(modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(12.dp), colors = CardDefaults.cardColors(containerColor = Color.White)) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text("Бак: ${container.id}", fontWeight = FontWeight.Bold)
                Box(modifier = Modifier.background(colorIndicator, RoundedCornerShape(6.dp)).padding(horizontal = 8.dp, vertical = 4.dp)) {
                    Text("${container.fillLevel}%", color = Color.White, fontWeight = FontWeight.Bold)
                }
            }
            Text("Пристрій: ${container.deviceId} | Тип: ${container.wasteTypeId}", modifier = Modifier.padding(vertical = 8.dp))
            Button(onClick = onClean, modifier = Modifier.fillMaxWidth()) {
                Text("Позначити як очищений")
            }
        }
    }
}