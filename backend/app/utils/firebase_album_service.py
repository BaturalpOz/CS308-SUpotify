import firebase_admin
from firebase_admin import credentials, firestore
from app.models.Album import Album  # Assuming your Album class is in 'app.models.album'
import os
from typing import Dict

class FirebaseAlbumService:
    def __init__(self):
        if not firebase_admin._apps:
            cred_path = os.getenv('FIREBASE_ADMINSDK_JSON_PATH')
            if cred_path is None:
                raise ValueError("The FIREBASE_ADMINSDK_JSON_PATH environment variable must be set.")
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)

        self.db = firestore.client()

    def add_album(self, album: Album):
        """
        Adds a new album document to the Albums collection.
        """
        # Convert the Album object to a dict suitable for Firestore
        album_dict = album.to_dict()
        try:
            # Create a new document in the 'Albums' collection with a unique ID
            _, doc_ref = self.db.collection(u'Albums').add(album_dict)
            return doc_ref.id  # Return the generated document ID
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_album_by_name(self, name: str):
        """
        Retrieves an album document from the Albums collection by name.
        """
        try:
            # Query for documents in the 'Albums' collection where the name matches
            albums_ref = self.db.collection(u'Albums')
            query = albums_ref.where(u'name', u'==', name)
            results = query.stream()
            for doc in results:
                # Convert the document to an Album object
                return Album.from_dict(doc.to_dict())
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_album(self, album_id: str):
        """
        Retrieves an album document from the Albums collection by album ID.
        """
        try:
            album_ref = self.db.collection(u'Albums').document(album_id)
            album_doc = album_ref.get()
            if album_doc.exists:
                return Album.from_dict(album_doc.to_dict())
            else:
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def update_album(self, album_id: str, update_data: Dict):
        """
        Updates an album document in the Albums collection.
        """
        try:
            album_ref = self.db.collection(u'Albums').document(album_id)
            album_ref.update(update_data)
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def delete_album(self, album_id: str):
        """
        Deletes an album document from the Albums collection.
        """
        try:
            album_ref = self.db.collection(u'Albums').document(album_id)
            album_ref.delete()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def get_all_album_ids(self):
        """
        Retrieves all album IDs from Firebase.
        """
        albums_ref = self.db.collection(u'Albums')
        return [doc.id for doc in albums_ref.stream()]
