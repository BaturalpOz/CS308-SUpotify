package com.example.supotify

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.app.AlertDialog

class DeleteSongActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_deletesong)
        supportActionBar?.title = "SUpotify"

        val songIdEditText = findViewById<EditText>(R.id.songId)
        val deleteButton = findViewById<Button>(R.id.deleteSongButton)

        deleteButton.setOnClickListener {
            val songId = songIdEditText.text.toString()

            if (songId.isEmpty()) {
                showAlertDialog("Please enter Song ID to delete.")
            } else {
                showAlertDialog("Song with ID $songId deleted successfully!")
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
