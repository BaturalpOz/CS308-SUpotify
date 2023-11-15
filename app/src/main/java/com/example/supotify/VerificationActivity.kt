package com.example.supotify
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import androidx.appcompat.app.AppCompatActivity
import android.content.Intent
import androidx.appcompat.app.AlertDialog

class VerificationActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_verification)

        val verificationCodeEditText = findViewById<EditText>(R.id.code)
        val verifyButton = findViewById<Button>(R.id.verifyButton)

        verifyButton.setOnClickListener {
            val verificationCode = verificationCodeEditText.text.toString()

            if (verificationCode.isEmpty()) {
                showAlertDialog("Verification code cannot be empty!")
            } else {
                // Doğrulama kodunu kontrol etme işlemleri burada gerçekleştirilebilir
                // Örneğin, doğrulama kodunu sunucuya gönderme ve doğrulama işlemini gerçekleştirme
                openMainActivity()
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

    private fun openMainActivity() {
        val intent = Intent(this, MainActivity::class.java)
        startActivity(intent)
        finish() // Geri dönüşü olmayan bir ekran olduğu için bu ekranı kapat
    }
}
