package com.example.passenger_app

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query

@Dao
interface PassengerDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(passenger: Passenger): Long

    @Query("SELECT * FROM Passenger")
    suspend fun getAll(): List<Passenger>

    @Query("SELECT * FROM Passenger where email = :email")
    suspend fun getByEmail(email: String): List<Passenger>
}