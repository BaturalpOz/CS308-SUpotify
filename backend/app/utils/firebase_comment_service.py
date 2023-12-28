import firebase_admin
from firebase_admin import credentials, firestore
from app.models.Comment import Comment  # Adjust the import statement based on your folder structure
import os
from typing import Dict, Optional


class FirebaseCommentService:
    def __init__(self):
        if not firebase_admin._apps:
            cred_path = os.getenv('FIREBASE_ADMINSDK_JSON_PATH')
            if cred_path is None:
                raise ValueError("The FIREBASE_ADMINSDK_JSON_PATH environment variable must be set.")
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)

        self.db = firestore.client()

    def send_comment(self, comment: Comment):
        """
        Adds a new comment document to the Comments collection.
        """
        try:
            # Convert the Comment object to a dict suitable for Firestore
            comment_dict = comment.to_dict()

            # Create a new document in the 'Comments' collection with a unique ID
            _, doc_ref = self.db.collection(u'Comments').add(comment_dict)

            print(f"Comment added successfully with ID: {doc_ref.id}")
            return doc_ref.id  # Return the generated document ID
        except Exception as e:
            print(f"An error occurred while adding comment: {e}")
            print(f"Comment details: {comment.to_dict()}")
            raise  # Reraise the exception for better debugging
    def get_comment(self, comment_id: str):
        """
        Retrieves a song document from the Songs collection by song ID.
        """
        try:
            comment_ref = self.db.collection(u'Comments').document(comment_id)
            comment_doc = comment_ref.get()
            if comment_doc.exists:
                return Comment.from_dict(comment_doc.to_dict())
            else:
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_all_comment_ids(self):
        """
        Retrieves all comment IDs from the Comments collection.
        """
        try:
            comment_ids = []
            comments_ref = self.db.collection(u'Comments').stream()
            for comment in comments_ref:
                comment_ids.append(comment.id)
            return comment_ids
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

