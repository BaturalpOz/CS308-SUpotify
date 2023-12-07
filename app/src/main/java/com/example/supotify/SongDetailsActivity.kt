// SongDetailsActivity.kt

package com.example.supotify

import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class SongDetailsActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_songdetails)

        val selectedSong = intent.getStringExtra("selectedSong")

        val songDetailsTextView = findViewById<TextView>(R.id.songDetailsTextView)
        songDetailsTextView.text = "Selected Song: $selectedSong"
    }
}
