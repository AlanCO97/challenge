package com.example.passenger_app

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import com.example.passenger_app.ui.theme.Passenger_appTheme
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
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


@Composable
fun PassengerApp() {
    Passenger_appTheme {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            val context = LocalContext.current

            val db = remember {
                Room.databaseBuilder(
                    context.applicationContext,
                    DatabaseObject::class.java, "passengers"
                ).allowMainThreadQueries().build()
            }

            val passengerDao = remember { db.passengerDao() }

            var name by remember { mutableStateOf("") }
            var email by remember { mutableStateOf("") }
            var errorMessage by remember { mutableStateOf("") }
            var successMessage by remember { mutableStateOf("") }
            var passengerInserted by remember { mutableStateOf(false) }

            val coroutineScope = rememberCoroutineScope()

            var passengers by remember { mutableStateOf(emptyList<Passenger>()) }
            LaunchedEffect(passengerInserted) {
                passengers = passengerDao.getAll()
                passengerInserted = false
            }

            val passengerCount = passengers.size

            Text(
                text = "Total de pasajeros: $passengerCount",
                modifier = Modifier.align(Alignment.Start).padding(bottom = 16.dp),
            )

            TextField(
                value = name,
                onValueChange = { name = it },
                label = {
                    Text(text = "Ingresa tu nombre")
                },
                placeholder = {
                    Text(text = "Nombre")
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(bottom = 16.dp)
            )

            TextField(
                value = email,
                onValueChange = { email = it },
                label = {
                    Text(text = "Ingresa tu correo")
                },
                placeholder = {
                    Text(text = "Correo electronico")
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(bottom = 16.dp)
            )

            if (errorMessage.isNotEmpty()) {
                Text(
                    text = errorMessage,
                    color = androidx.compose.ui.graphics.Color.Red,
                    modifier = Modifier.padding(bottom = 16.dp)
                )
            }

            if (successMessage.isNotEmpty()) {
                Text(
                    text = successMessage,
                    color = androidx.compose.ui.graphics.Color.Black,
                    modifier = Modifier.padding(bottom = 16.dp)
                )
                LaunchedEffect(Unit) {
                    delay(3000L)
                    successMessage = ""
                }
            }
            
            Button(
                onClick = {
                    coroutineScope.launch {
                        if (name.isBlank() || email.isBlank()) {
                            errorMessage = "Nombre y correo son requeridos"
                        } else {
                            val existingPassengers = passengerDao.getByEmail(email)
                            if (existingPassengers.isNotEmpty()) {
                                errorMessage = "Ya existe un pasajero con este correo"
                            } else {
                                if (passengerCount >= 10) {
                                    errorMessage = "No se pueden agregar más pasajeros"
                                } else {
                                    val passenger = Passenger(name = name, email = email)
                                    passengerDao.insert(passenger)
                                    name = ""
                                    email = ""
                                    errorMessage = ""
                                    successMessage = "¡Datos guardados exitosamente!"
                                    passengerInserted = true
                                }
                            }
                        }
                    }
                },
                enabled = passengerCount < 10,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(bottom = 16.dp)
            ) {
                Text(text = "Guardar")
            }

            Button(
                onClick = {
                    println("se enviaran los registros al servidor")
                },
                modifier = Modifier.fillMaxWidth()) {
                Text(text = "Enviar al servidor")
            }

        }
    }
}