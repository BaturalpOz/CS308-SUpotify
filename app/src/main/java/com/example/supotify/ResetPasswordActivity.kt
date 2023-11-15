package com.example.supotify
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import androidx.appcompat.app.AppCompatActivity
import android.content.Intent
import android.widget.TextView
import androidx.appcompat.app.AlertDialog

class ResetPasswordActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_reset_password)

        val emailEditText = findViewById<EditText>(R.id.email)
        val resetPasswordButton = findViewById<Button>(R.id.resetPasswordButton)
        val backToSignIn = findViewById<TextView>(R.id.backToSignIn)

        resetPasswordButton.setOnClickListener {
            val email = emailEditText.text.toString()

            if (email.isEmpty()) {
                showAlertDialog("Email cannot be empty!")
            } else {
                // Şifre sıfırlama işlemleri burada gerçekleştirilebilir
                // Örneğin, e-posta adresine şifre sıfırlama bağlantısı gönderme veya doğrulama kodunu kontrol etme
                openVerificationActivity()
            }
        }

        backToSignIn.setOnClickListener {
            openLoginActivity()
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

    private fun openVerificationActivity() {
        val intent = Intent(this, VerificationActivity::class.java)
        startActivity(intent)
    }

    private fun openLoginActivity() {
        val intent = Intent(this, LoginActivity::class.java)
        startActivity(intent)
        finish() // Bu, ResetPasswordActivity'yi kapatır ve geri tuşuna basıldığında tekrar buraya gelinmez.
    }
}
