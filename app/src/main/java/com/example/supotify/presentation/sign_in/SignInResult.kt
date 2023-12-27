// SignInResult.kt
package com.example.supotify.presentation.sign_in

data class SignInResult(
    val data: UserData?,
    val errorMessage: String?
) {
    val isSuccess: Boolean
        get() = data != null
}


data class UserData(
    val userId: String,
    val username: String?,
    val profilePictureUrl: String?
)
