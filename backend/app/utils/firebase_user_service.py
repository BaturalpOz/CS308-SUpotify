import firebase_admin
from firebase_admin import credentials, firestore
from app.models.User import User
import os
from typing import Dict

class FirebaseUserService:
    def __init__(self):
        if not firebase_admin._apps:
            cred_path = os.getenv('FIREBASE_ADMINSDK_JSON_PATH')
            if cred_path is None:
                raise ValueError("The FIREBASE_ADMINSDK_JSON_PATH environment variable must be set.")
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)

        self.db = firestore.client()

    def add_user(self, user: User):
        """
        Adds a new user document to the Users collection.
        """
        # Convert the User object to a dict suitable for Firestore
        user_dict = user.to_dict()
        try:
            # Create a new document in the 'Users' collection with a unique ID
            _, doc_ref = self.db.collection(u'Users').add(user_dict)
            return doc_ref.id  # Return the generated document ID
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_user_by_username(self, username: str):
        """
        Retrieves a user document from the Users collection by username.
        """
        try:
            # Query for documents in the 'Users' collection where the username matches
            users_ref = self.db.collection(u'Users')
            query = users_ref.where(u'username', u'==', username)
            results = query.stream()
            for doc in results:
                # Convert the document to a User object
                user = User.from_dict(doc.to_dict())
                user.user_id = doc.id
                return user
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_by_email(self, email: str):
        """
        Retrieves a user document from the Users collection by email.
        """
        try:
            # Query for documents in the 'Users' collection where the email matches
            users_ref = self.db.collection(u'Users')
            query = users_ref.where(u'email', u'==', email)
            results = query.stream()
            for doc in results:
                # Convert the document to a User object
                user = User.from_dict(doc.to_dict())
                user.user_id = doc.id
                return user
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_user(self, user_id: str):
        """
        Retrieves a user document from the Users collection by user ID.
        """
        try:
            user_ref = self.db.collection(u'Users').document(user_id)
            user_doc = user_ref.get()
            #print firebase document id
            print(u'Document data: {}'.format(user_doc.id))
            if user_doc.exists:
                # Convert the document to a User object
                user = User.from_dict(user_doc.to_dict())
                user.user_id = user_doc.id
                return user
            else:
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def update_user(self, user_id: str, update_data: Dict):
        """
        Updates a user document in the Users collection.
        """
        try:
            user_ref = self.db.collection(u'Users').document(user_id)
            user_ref.update(update_data) 
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        
    def delete_user(self, user_id: str):
        """
        Deletes a user document from the Users collection.
        """
        try:
            user_ref = self.db.collection(u'Users').document(user_id)
            user_ref.delete()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        