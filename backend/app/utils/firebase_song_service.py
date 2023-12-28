from ast import List
import firebase_admin
from firebase_admin import credentials, firestore
from app.models.Song import Song
import os
from typing import Dict
import Levenshtein


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

    def get_song(self, song_id: int):
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

    def get_song_id_by_name(self,name:str):
        """
        Retrieves a song document from the Songs collection by name.
        """
        try:
            
            song_ref = self.db.collection(u'Songs')
            query = song_ref.where(u'Name', u'==', name)
            song_id = query.get()[0].id
           

            return song_id

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def get_song_by_name(self, name: str):
        """
        Retrieves a song document from the Songs collection by name.
        """
        try:

            song_ref = self.db.collection(u'Songs')
            query = song_ref.where(u'Name', u'==', name)
            results = query.get()

            return Song.from_dict(results[0].to_dict())

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

    def get_all_song_ids(self):
        """
        Retrieves all song IDs from the Songs collection.
        """
        try:
            song_ids = []
            songs_ref = self.db.collection(u'Songs').stream()
            for song in songs_ref:
                song_ids.append(song.id)
            return song_ids
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def get_all_songs(self):
        try:
            song_list = []
            song_docs = self.db.collection(u'Songs').stream()
            for doc in song_docs:
                dict_song = doc.to_dict()
                #song = Song.from_dict(dict_song)
                dict_song["Id"] = doc.id
                song_list.append(dict_song)
            return song_list
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def get_song_count(self):
        songs_ref = self.db.collection(u'Songs')
        snapshot = songs_ref.count().get()
        count = snapshot[0][0].value
        return count
            
    def search_songs(self, query: str, max_distance: int = 2):
        """
        Search for songs based on Levenshtein distance to the query in name, albums, or artists.
        """
        try:
            songs_ref = self.db.collection(u'Songs').stream()
            all_songs = [song for song in songs_ref]
            
            matching_songs = []

            for song in all_songs:
                song = song.to_dict()
                distance = Levenshtein.distance(song.get('Name', '').lower(), query.lower())
                if (distance<= max_distance):
                    matching_songs.append({"song":song, "_similarity": distance})
            matching_songs.sort(key=lambda x: x["_similarity"])
            albums_ref = self.db.collection(u'Albums').stream()
            all_albums = [album for album in albums_ref]

            matching_albums = []
            for album in all_albums:
                album = album.to_dict()
                distance = Levenshtein.distance(album.get('Name', '').lower(), query.lower())
                if (distance<= max_distance):
                    matching_albums.append({"album":album, "_similarity": distance})
            matching_albums.sort(key=lambda x: x["_similarity"])
            artists_ref = self.db.collection(u'Artists').stream()
            all_artists = [artist for artist in artists_ref]

            matching_artists = []

            for artist in all_artists:
                artist = artist.to_dict()
                distance = Levenshtein.distance(artist.get('Name', '').lower(), query.lower())
                if (distance <= max_distance):
                    matching_artists.append({"artist":artist, "_similarity": distance})
            matching_songs.sort(key=lambda x: x["_similarity"])

            return {"songs": matching_songs[:5], "albums": matching_albums[:2], "artists": matching_artists[:2]}

        except Exception as e:
            print(f"An error occurred: {e}")
            return []
