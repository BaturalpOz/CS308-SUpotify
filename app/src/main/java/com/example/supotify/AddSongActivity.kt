package com.example.supotify

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.app.AlertDialog

class AddSongActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_addsong)

        val songTitleEditText = findViewById<EditText>(R.id.songTitle)
        val artistNameEditText = findViewById<EditText>(R.id.artistName)
        val albumNameEditText = findViewById<EditText>(R.id.albumName)
        val releaseDateEditText = findViewById<EditText>(R.id.releaseDate)
        val songLengthEditText = findViewById<EditText>(R.id.songLength)
        val submitSongButton = findViewById<Button>(R.id.submitSongButton)

        submitSongButton.setOnClickListener {
            val songTitle = songTitleEditText.text.toString()
            val artistName = artistNameEditText.text.toString()
            val albumName = albumNameEditText.text.toString()
            val releaseDate = releaseDateEditText.text.toString()
            val songLength = songLengthEditText.text.toString()

            if (songTitle.isEmpty() || artistName.isEmpty() || albumName.isEmpty() || releaseDate.isEmpty() || songLength.isEmpty()) {
                showAlertDialog("Please fill in all fields.")
            } else {
                val songInfo = "Title: $songTitle\nArtist: $artistName\nAlbum: $albumName\nRelease Date: $releaseDate\nLength: $songLength"
                showSongDetailsDialog(songInfo)
            }
        }
    }

    private fun showAlertDialog(message: String) {
        val builder: AlertDialog.Builder = AlertDialog.Builder(this)
        builder.setMessage(message)
            .setCancelable(false)
            .setPositiveButton("OK") { dialog, _ ->
                dialog.dismiss()
            }
        val alert: AlertDialog = builder.create()
        alert.setTitle("Alert")
        alert.show()
    }

    private fun showSongDetailsDialog(songInfo: String) {
        val builder: AlertDialog.Builder = AlertDialog.Builder(this)
        builder.setMessage(songInfo)
            .setCancelable(false)
            .setPositiveButton("OK") { dialog, _ ->
                dialog.dismiss()
            }
        val alert: AlertDialog = builder.create()
        alert.setTitle("Song Details")
        alert.show()
    }
}
