package com.example.supotify

import android.os.Bundle
import android.content.Intent
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login) // Güncellenmiş layout dosyası adı

        // Burada login sayfasına geçiş yapacak kodlar olacak
        val intent = Intent(this, LoginActivity::class.java)
        startActivity(intent)
    }
}
