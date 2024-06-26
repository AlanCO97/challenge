package com.example.passenger_app

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(indices = [Index(value = ["email"], unique = true)])
data class Passenger(
    @PrimaryKey(autoGenerate = true) var id: Int = 0,
    @ColumnInfo(name="name") var name: String,
    @ColumnInfo(name="email") var email: String
)
