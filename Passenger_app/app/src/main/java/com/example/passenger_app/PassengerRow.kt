package com.example.passenger_app

import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.Button
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material.icons.outlined.Create
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.Alignment

@Composable
fun PassengerRow(
    passenger: Passenger,
    onDelete: () -> Unit,
    onUpdate: (String, String) -> Unit
) {
    Row(
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier
            .padding(bottom = 4.dp)
            .fillMaxWidth()
    ) {
        Text(
            text = "${passenger.name}, ${passenger.email}",
            modifier = Modifier.weight(1f)
        )
        Row {
            Button(
                onClick = onDelete,
                modifier = Modifier.padding(end = 8.dp)
            ) {
                Icon(Icons.Outlined.Delete, contentDescription = "Eliminar")
            }

            Button(
                onClick = { onUpdate(passenger.name, passenger.email) }
            ) {
                Icon(Icons.Outlined.Create, contentDescription = "Actualizar")
            }
        }
    }
}
