package com.example.supotify

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.app.AlertDialog

class UpdateSongActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_updatesong)
        supportActionBar?.title = "SUpotify"

        val songTitleEditText = findViewById<EditText>(R.id.songTitle)
        val artistNameEditText = findViewById<EditText>(R.id.artistName)
        val albumNameEditText = findViewById<EditText>(R.id.albumName)
        val releaseDateEditText = findViewById<EditText>(R.id.releaseDate)
        val songLengthEditText = findViewById<EditText>(R.id.songLength)
        val submitButton = findViewById<Button>(R.id.submitSongButton)

        submitButton.setOnClickListener {
            val songTitle = songTitleEditText.text.toString()
            val artistName = artistNameEditText.text.toString()
            val albumName = albumNameEditText.text.toString()
            val releaseDate = releaseDateEditText.text.toString()
            val songLength = songLengthEditText.text.toString()

            if (songTitle.isEmpty() || artistName.isEmpty() || albumName.isEmpty() ||
                releaseDate.isEmpty() || songLength.isEmpty()) {
                showAlertDialog("All fields are required!")
            } else {
                // Güncelleme işlemleri burada gerçekleştirilebilir
                // Örneğin, veritabanında şarkıyı güncelleme
                showAlertDialog("Song updated successfully!")
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
}
