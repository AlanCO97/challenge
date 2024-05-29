package com.example.passenger_app

import androidx.room.Database
import androidx.room.RoomDatabase

@Database(entities = [Passenger::class], version = 1)
abstract class DatabaseObject : RoomDatabase() {
    abstract fun passengerDao(): PassengerDao
}