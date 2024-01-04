package com.example.supotify

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class ForumActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_forum)

        supportActionBar?.hide()

        // User Comments Section
        val commentsSection: LinearLayout = findViewById(R.id.commentsSection)
        val userCommentsTitle: TextView = findViewById(R.id.userCommentsTitle)
        val addCommentForm: LinearLayout = findViewById(R.id.addCommentForm)
        val commentEditText: EditText = findViewById(R.id.commentEditText)
        val postCommentButton: Button = findViewById(R.id.postCommentButton)
        val commentsContainer: LinearLayout = findViewById(R.id.commentsContainer)

        // Add Comment Button Click Listener
        postCommentButton.setOnClickListener {
            postComment(commentEditText.text.toString(), commentsContainer)
        }

    }

    private fun postComment(commentText: String, commentsContainer: LinearLayout) {
        // Add a new TextView to commentsContainer with the new comment
        val newCommentTextView = TextView(this)
        newCommentTextView.text = commentText
        commentsContainer.addView(newCommentTextView)


    }

}
