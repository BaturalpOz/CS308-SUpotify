package com.example.supotify

import android.content.Intent
import android.os.Bundle
import com.example.supotify.presentation.sign_in.GoogleAuthUiClient
import com.example.supotify.presentation.sign_in.SignInViewModel
import android.text.InputType
import android.widget.Button
import android.content.IntentSender
import android.widget.EditText
import android.widget.TextView
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import android.widget.ToggleButton
import com.google.android.gms.auth.api.identity.Identity
import com.example.supotify.presentation.sign_in.SignInResult
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.MainScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class LoginActivity : AppCompatActivity(), CoroutineScope by MainScope() {

    private val REQUEST_CODE_GOOGLE_SIGN_IN = 1001

    private val googleAuthUiClient by lazy {
        GoogleAuthUiClient(
            context = applicationContext,
            oneTapClient = Identity.getSignInClient(applicationContext)
        )
    }

    private val signInViewModel by lazy {
        SignInViewModel()
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        val emailEditText = findViewById<EditText>(R.id.email)
        val passwordEditText = findViewById<EditText>(R.id.oldPassword)
        val loginButton = findViewById<Button>(R.id.changePasswordButton)
        val signUpHint = findViewById<TextView>(R.id.signUpHint)
        val togglePasswordVisibility = findViewById<ToggleButton>(R.id.togglePasswordVisibility)
        val forgotPassword = findViewById<TextView>(R.id.forgotPassword)
        val googleSignInButton = findViewById<Button>(R.id.googleSignInButton)

        var isPasswordVisible = false

        togglePasswordVisibility.setOnCheckedChangeListener { _, isChecked ->
            isPasswordVisible = isChecked
            updatePasswordVisibility(passwordEditText, isPasswordVisible)
        }

        signUpHint.setOnClickListener {
            val intent = Intent(this, CreateAccountActivity::class.java)
            startActivity(intent)
        }

        loginButton.setOnClickListener {
            val email = emailEditText.text.toString()
            val password = passwordEditText.text.toString()

            if (email.isEmpty() || password.isEmpty()) {
                showAlertDialog()
            } else {
                openCategoryActivity()
            }
        }

        forgotPassword.setOnClickListener {
            val intent = Intent(this, ResetPasswordActivity::class.java)
            startActivity(intent)
        }

        googleSignInButton.setOnClickListener {
            launch {
                signInWithGoogle()
            }
        }
    }

    private suspend fun signInWithGoogle() {
        val signInIntentSender = googleAuthUiClient.signIn()
        if (signInIntentSender != null) {
            try {
                startIntentSenderForResult(
                    signInIntentSender,
                    REQUEST_CODE_GOOGLE_SIGN_IN,
                    null,
                    0,
                    0,
                    0,
                    null
                )
            } catch (e: IntentSender.SendIntentException) {
                e.printStackTrace()
            }
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        if (requestCode == REQUEST_CODE_GOOGLE_SIGN_IN) {
            launch(Dispatchers.IO) {
                val signInResult = googleAuthUiClient.signInWithIntent(data ?: return@launch)
                withContext(Dispatchers.Main) {
                    handleSignInResult(signInResult)
                }
            }
        }
    }

    private fun handleSignInResult(signInResult: SignInResult?) {
        signInResult?.let {
            signInViewModel.onSignInResult(it)

            if (it.isSuccess) {
                openCategoryActivity()
            } else {
                showSignInError(it.errorMessage ?: "Unknown error")
            }
        }
    }

    private fun showSignInError(errorMessage: String) {
        val builder: AlertDialog.Builder = AlertDialog.Builder(this)
        builder.setMessage(errorMessage)
            .setCancelable(false)
            .setPositiveButton("OK") { dialog, _ ->
                dialog.dismiss()
            }
        val alert: AlertDialog = builder.create()
        alert.setTitle("Sign-In Error")
        alert.show()
    }

    private fun updatePasswordVisibility(editText: EditText, isVisible: Boolean) {
        if (isVisible) {
            editText.inputType = InputType.TYPE_TEXT_VARIATION_VISIBLE_PASSWORD
        } else {
            editText.inputType = InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_PASSWORD
        }
        editText.setSelection(editText.text.length)
    }

    private fun showAlertDialog() {
        val builder: AlertDialog.Builder = AlertDialog.Builder(this)
        builder.setMessage("Email or password cannot be empty!")
            .setCancelable(false)
            .setPositiveButton("OK") { dialog, _ ->
                dialog.dismiss()
            }
        val alert: AlertDialog = builder.create()
        alert.setTitle("Alert")
        alert.show()
    }

    private fun openCategoryActivity() {
        val intent = Intent(this, CategoryActivity::class.java)
        startActivity(intent)
    }
}
