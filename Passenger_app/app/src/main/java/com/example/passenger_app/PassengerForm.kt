package com.example.passenger_app

import androidx.compose.foundation.layout.Column
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.ui.Alignment
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

import kotlinx.coroutines.CoroutineScope

@Composable
fun PassengerForm(
    name: String,
    onNameChange: (String) -> Unit,
    email: String,
    onEmailChange: (String) -> Unit,
    fromUpdate: Boolean,
    passengerDao: PassengerDao,
    coroutineScope: CoroutineScope,
    onPassengerInserted: () -> Unit,
    passengers: List<Passenger>,
    errorMessage: String,
    successMessage: String,
    setErrorMessage: (String) -> Unit,
    setSuccessMessage: (String) -> Unit,
    setFromUpdate: (Boolean) -> Unit
) {
    val passengerCount = passengers.size

    Column {
        Text(
            text = "Total de pasajeros: $passengerCount",
            modifier = Modifier
                .align(Alignment.Start)
                .padding(bottom = 16.dp),
        )

        TextField(
            value = name,
            onValueChange = onNameChange,
            label = { Text(text = "Ingresa tu nombre") },
            placeholder = { Text(text = "Nombre") },
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 16.dp)
        )

        TextField(
            value = email,
            onValueChange = onEmailChange,
            label = { Text(text = "Ingresa tu correo") },
            placeholder = { Text(text = "Correo electronico") },
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
                setSuccessMessage("")
            }
        }

        Button(
            onClick = {
                coroutineScope.launch {
                    if (name.isBlank() || email.isBlank()) {
                        setErrorMessage("Nombre y correo son requeridos")
                    } else {
                        if (fromUpdate) {
                            passengerDao.updateNameByEmail(email, name)
                            onNameChange("")
                            onEmailChange("")
                            setErrorMessage("")
                            setSuccessMessage("¡Datos actualizados exitosamente!")
                            onPassengerInserted()
                            setFromUpdate(false)
                        } else {
                            val existingPassengers = passengerDao.getByEmail(email)
                            if (existingPassengers.isNotEmpty()) {
                                setErrorMessage("Ya existe un pasajero con este correo")
                            } else {
                                if (passengerCount >= 10) {
                                    setErrorMessage("No se pueden agregar más pasajeros")
                                } else {
                                    val passenger = Passenger(name = name, email = email)
                                    passengerDao.insert(passenger)
                                    onNameChange("")
                                    onEmailChange("")
                                    setErrorMessage("")
                                    setSuccessMessage("¡Datos guardados exitosamente!")
                                    onPassengerInserted()
                                }
                            }
                        }
                    }
                }
            },
            enabled = passengerCount < 10 || fromUpdate,
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 16.dp)
        ) {
            Text(text = "Guardar")
        }

        Button(
            onClick = {
              println("Se mandaran los datos al servidor")
            },
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 16.dp)
        ) {
            Text(text = "Mandar al servidor")
        }
    }
}