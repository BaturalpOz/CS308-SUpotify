import android.content.DialogInterface
import android.os.Bundle
import com.example.supotify.R
import android.widget.Button
import android.widget.EditText
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity

class ChangePasswordActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_change_password)

        val changePasswordButton = findViewById<Button>(R.id.changePasswordButton)
        changePasswordButton.setOnClickListener {
            val emailEditText = findViewById<EditText>(R.id.email)
            val oldPasswordEditText = findViewById<EditText>(R.id.oldPassword)
            val newPasswordEditText = findViewById<EditText>(R.id.newPassword)
            val confirmNewPasswordEditText = findViewById<EditText>(R.id.confirmNewPassword)

            val email = emailEditText.text.toString()
            val oldPassword = oldPasswordEditText.text.toString()
            val newPassword = newPasswordEditText.text.toString()
            val confirmNewPassword = confirmNewPasswordEditText.text.toString()

            if (email.isEmpty() || oldPassword.isEmpty() || newPassword.isEmpty() || confirmNewPassword.isEmpty()) {
                showAlertDialog("Please fill in all fields.")
            } else if (newPassword != confirmNewPassword) {
                showAlertDialog("New password and confirm new password must match.")
            } else {
            }
        }
    }

    private fun showAlertDialog(message: String) {
        val builder: AlertDialog.Builder = AlertDialog.Builder(this)
        builder.setMessage(message)
            .setCancelable(false)
            .setPositiveButton("OK", DialogInterface.OnClickListener { dialog, _ ->
                dialog.dismiss()
            })
        val alert: AlertDialog = builder.create()
        alert.setTitle("Alert")
        alert.show()
    }
}
