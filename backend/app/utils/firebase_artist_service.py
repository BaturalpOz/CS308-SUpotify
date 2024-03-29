import firebase_admin
from firebase_admin import credentials, firestore
from app.models.Artist import Artist  
import os
from typing import Dict

class FirebaseArtistService:
    def __init__(self):
        if not firebase_admin._apps:
            cred_path = os.getenv('FIREBASE_ADMINSDK_JSON_PATH')
            if cred_path is None:
                raise ValueError("The FIREBASE_ADMINSDK_JSON_PATH environment variable must be set.")
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)

        self.db = firestore.client()

    def add_artist(self, artist: Artist):
        """
        Adds a new artist document to the Artists collection.
        """
      
        artist_dict = artist.to_dict()
        try:
            
            _, doc_ref = self.db.collection(u'Artists').add(artist_dict)
            return doc_ref.id  
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_artist_by_name(self, name: str):
        """
        Retrieves an artist document from the Artists collection by name.
        """
        try:
            artists_ref = self.db.collection(u'Artists')
            query = artists_ref.where(u'Name', u'==', name)
            results = query.get()
            dict_artist = results[0].to_dict()
            dict_artist["Id"] = results[0].id
            return dict_artist
           
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_artist(self, artist_id: str):
        """
        Retrieves an artist document from the Artists collection by artist ID.
        """
        try:
            artist_ref = self.db.collection(u'Artists').document(artist_id).get()
            
            if artist_ref.exists:
                artist_doc = artist_ref.to_dict()
               
            
                return Artist.from_dict(artist_doc)
            else:
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def update_artist(self, artist_id: str, update_data: Dict):
        """
        Updates an artist document in the Artists collection.
        """
        try:
            artist_ref = self.db.collection(u'Artists').document(artist_id)
            artist_ref.update(update_data)
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def delete_artist(self, artist_id: str):
        """
        Deletes an artist document from the Artists collection.
        """
        try:
            artist_ref = self.db.collection(u'Artists').document(artist_id)
            artist_ref.delete()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def get_all_artist_ids(self):
        """
        Retrieves all artist IDs from Firebase.
        """
        try:
            artists_ref = self.db.collection(u'Artists')
            query = artists_ref.select(['artist_id'])
            results = query.stream()
            return [doc.id for doc in results]
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
    def  get_all_artists(self):
        try:
            artist_list = []
            artists_docs = self.db.collection(u'Artists').stream()
            for doc in artists_docs:
                dict_artist = doc.to_dict()
                #artist = Artist.from_dict(dict_artist)
                dict_artist["Id"] = doc.id
                artist_list.append(dict_artist)
            return artist_list
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
            