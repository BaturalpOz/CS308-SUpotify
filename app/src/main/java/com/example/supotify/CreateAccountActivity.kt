package com.example.supotify

import android.content.DialogInterface
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity

class CreateAccountActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_create_account)

        val createButton = findViewById<Button>(R.id.buttonCreateAccount)
        createButton.setOnClickListener {
            val nameEditText = findViewById<EditText>(R.id.editTextName)
            val emailEditText = findViewById<EditText>(R.id.editTextEmail)
            val passwordEditText = findViewById<EditText>(R.id.editTextPassword)

            val name = nameEditText.text.toString()
            val email = emailEditText.text.toString()
            val password = passwordEditText.text.toString()

            if (name.isEmpty() || email.isEmpty() || password.isEmpty()) {
                val builder: AlertDialog.Builder = AlertDialog.Builder(this)
                builder.setMessage("Name, email, or password cannot be empty!")
                    .setCancelable(false)
                    .setPositiveButton("OK", DialogInterface.OnClickListener { dialog, _ ->
                        dialog.dismiss()
                    })
                val alert: AlertDialog = builder.create()
                alert.setTitle("Alert")
                alert.show()
            } else {
                // Proceed with account creation operations here
            }
        }
    }
}
