package com.example.smartsorter.ui.screen

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.unit.dp
import com.example.smartsorter.ui.viewmodel.DriverRouteViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AlertsScreen(viewModel: DriverRouteViewModel) {
    var message by remember { mutableStateOf(TextFieldValue("")) }
    var containerId by remember { mutableStateOf(TextFieldValue("")) }
    val alertStatus by viewModel.alertStatus.collectAsState()

    LaunchedEffect(Unit) {
        viewModel.resetAlertStatus()
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Відправити Звіт", color = Color.White) },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.primary)
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text("Звіт про проблему", style = MaterialTheme.typography.titleLarge)
            Spacer(modifier = Modifier.height(16.dp))
            
            OutlinedTextField(
                value = containerId,
                onValueChange = { containerId = it },
                label = { Text("ID Контейнера (необов'язково)") },
                modifier = Modifier.fillMaxWidth()
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            OutlinedTextField(
                value = message,
                onValueChange = { message = it },
                label = { Text("Повідомлення") },
                modifier = Modifier.fillMaxWidth().height(150.dp),
                maxLines = 5
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Button(
                onClick = {
                    val id = containerId.text.toIntOrNull()
                    viewModel.submitAlert(message.text, id)
                },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Відправити")
            }

            if (alertStatus.isNotEmpty()) {
                Spacer(modifier = Modifier.height(16.dp))
                Text(alertStatus, color = if (alertStatus.contains("успішно")) Color(0xFF2E7D32) else MaterialTheme.colorScheme.error)
            }
        }
    }
}
