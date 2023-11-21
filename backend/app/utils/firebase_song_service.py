import firebase_admin
from firebase_admin import credentials, firestore
from app.models.Song import Song
import os
from typing import Dict


class FirebaseSongService:
    def __init__(self):
        if not firebase_admin._apps:
            cred_path = os.getenv('FIREBASE_ADMINSDK_JSON_PATH')
            if cred_path is None:
                raise ValueError("The FIREBASE_ADMINSDK_JSON_PATH environment variable must be set.")
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            
        self.db = firestore.client()

    def add_song(self, song: Song):
        """
        Adds a new song document to the Songs collection.
        """
        # Convert the Song object to a dict suitable for Firestore
        song_dict = song.to_dict()
        try:
            # Create a new document in the 'Songs' collection with a unique ID
            _, doc_ref = self.db.collection(u'Songs').add(song_dict)
            return doc_ref.id  # Return the generated document ID
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_song_by_id(self, song_id: int):
        """
        Retrieves a song document from the Songs collection by song ID.
        """
        try:
            song_ref = self.db.collection(u'Songs').document(song_id)
            song_doc = song_ref.get()
            if song_doc.exists:
                return Song.from_dict(song_doc.to_dict())
            else:
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def update_song(self, song_id: str, update_data: Dict):
        """
        Updates a song document in the Songs collection.
        """
        try:
            song_ref = self.db.collection(u'Songs').document(song_id)
            song_ref.update(update_data)
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def delete_song(self, song_id: str):
        """
        Deletes a song document from the Songs collection.
        """
        try:
            song_ref = self.db.collection(u'Songs').document(song_id)
            song_ref.delete()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
