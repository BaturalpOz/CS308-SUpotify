import firebase_admin
from firebase_admin import credentials, firestore
from app.models.Album import Album  
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
     
        album_dict = album.to_dict()
        try:
        
            _, doc_ref = self.db.collection(u'Albums').add(album_dict)
            return doc_ref.id  
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_album_by_name(self, name: str):
        """
        Retrieves an album document from the Albums collection by name.
        """
        try:
         
            albums_ref = self.db.collection(u'Albums')
            query = albums_ref.where(u'Name', u'==', name)
            results = query.get()
         
            return Album.from_dict(results[0].to_dict())
          
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
