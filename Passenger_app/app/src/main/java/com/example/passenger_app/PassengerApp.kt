package com.example.passenger_app

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import com.example.passenger_app.ui.theme.Passenger_appTheme
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.room.Room
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Create
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material3.Icon
import androidx.compose.runtime.produceState


@Composable
fun PassengerApp() {
    var passengers by remember { mutableStateOf(emptyList<Passenger>()) }
    val coroutineScope = rememberCoroutineScope()
    val context = LocalContext.current
    val db = remember {
        Room.databaseBuilder(
            context.applicationContext,
            DatabaseObject::class.java, "passengers"
        ).build()
    }
    val passengerDao = remember { db.passengerDao() }
    var name by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var fromUpdate by remember { mutableStateOf(false) }

    Passenger_appTheme {
        // Wrapping content inside LazyColumn to make it scrollable
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            item {
                var errorMessage by remember { mutableStateOf("") }
                var successMessage by remember { mutableStateOf("") }
                var passengerInserted by remember { mutableStateOf(false) }

                LaunchedEffect(passengerInserted) {
                    passengers = passengerDao.getAll()
                    passengerInserted = false
                }

                PassengerForm(
                    name = name,
                    onNameChange = { name = it },
                    email = email,
                    onEmailChange = { email = it },
                    fromUpdate = fromUpdate,
                    passengerDao = passengerDao,
                    coroutineScope = coroutineScope,
                    onPassengerInserted = { passengerInserted = true },
                    passengers = passengers,
                    errorMessage = errorMessage,
                    successMessage = successMessage,
                    setErrorMessage = { errorMessage = it },
                    setSuccessMessage = { successMessage = it },
                    setFromUpdate = { fromUpdate = it }
                )
            }

            items(passengers) { passenger ->
                PassengerRow(
                    passenger = passenger,
                    onDelete = {
                        coroutineScope.launch {
                            passengerDao.deleteByEmail(passenger.email)
                            passengers = passengerDao.getAll()
                        }
                    },
                    onUpdate = { selectedName, selectedEmail ->
                        name = selectedName
                        email = selectedEmail
                        fromUpdate = true
                    }
                )
            }
        }
    }
}
