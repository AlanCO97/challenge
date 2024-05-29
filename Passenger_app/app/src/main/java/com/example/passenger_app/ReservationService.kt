package com.example.passenger_app

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.POST

private const val BASE_URL = "http://10.0.2.2:8000/api/"

private val retrofit = Retrofit.Builder()
    .addConverterFactory(GsonConverterFactory.create())
    .baseUrl(BASE_URL)
    .build()

interface ReservationService {
    @POST("passengers/bulk")
    suspend fun bulkCreate(@Body passengers: List<Passenger>): List<Passenger>
}

object ApiClient {
    val reservationService: ReservationService by lazy {
        retrofit.create(ReservationService::class.java)
    }
}