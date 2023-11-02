package com.example.supotify

import android.content.DialogInterface
import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity

class LoginActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        val createAccountLink = findViewById<TextView>(R.id.createAccountLink)
        createAccountLink.setOnClickListener {
            val intent = Intent(this, CreateAccountActivity::class.java)
            startActivity(intent)
        }

        val loginButton = findViewById<Button>(R.id.buttonLogin)
        loginButton.setOnClickListener {
            val usernameEditText = findViewById<EditText>(R.id.editTextUsername)
            val passwordEditText = findViewById<EditText>(R.id.editTextPassword)

            val username = usernameEditText.text.toString()
            val password = passwordEditText.text.toString()

            if (username.isEmpty() || password.isEmpty()) {
                val builder: AlertDialog.Builder = AlertDialog.Builder(this)
                builder.setMessage("Username or password cannot be empty!")
                    .setCancelable(false)
                    .setPositiveButton("OK", DialogInterface.OnClickListener { dialog, _ ->
                        dialog.dismiss()
                    })
                val alert: AlertDialog = builder.create()
                alert.setTitle("Alert")
                alert.show()
            } else {
                // Proceed with login operations here
            }
        }
    }
}
