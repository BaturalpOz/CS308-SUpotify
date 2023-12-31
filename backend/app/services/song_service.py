from app.utils.firebase_song_service import FirebaseSongService
from app.models.Song import Song
from datetime import datetime
from typing import List


class SongService:
    def __init__(self):
        self.firebase_song_service = FirebaseSongService()

    def add_song(self, name: str, duration: int, danceability: float, energy: float, loudness: float, tempo: float, albums: List[str], artists: List[str]):
        """
        Handles the business logic for adding a new song.
        """
        new_song = Song(
            name=name,
            duration_ms=duration,
            danceability=danceability,
            energy=energy,
            loudness=loudness,
            tempo=tempo,
            albums=albums,
            artists=artists
        )

       
        song_id = self.firebase_song_service.add_song(new_song)

        if song_id:
            return song_id
        else:
            raise Exception("Failed to add a new song in Firebase.")

    def get_song_by_id(self, song_id: str):
        """
        Retrieves a song by its unique song ID.
        """
        if not song_id:
            raise ValueError("song ID cannot be empty.")
        elif not self.firebase_song_service.get_song(song_id):
            raise ValueError("song does not exist.")
        return self.firebase_song_service.get_song(song_id)

    def get_song_by_name(self, name: str):
        """
        Retrieves a song by its unique name.
        """
        if not name:
            raise ValueError("Name cannot be empty.")
        elif not self.firebase_song_service.get_song_by_name(name):
            raise ValueError("Album does not exist.")
        return self.firebase_song_service.get_song_by_name(name)

    def update_song(self, song_id: str, update_data: dict):
        """
        Updates song information given the song ID and the new data.
        """
        success = self.firebase_song_service.update_song(song_id, update_data)

        if not success:
            raise Exception("Failed to update the song.")

    def delete_song(self, song_id: str):
        """
        Deletes a song by its unique song ID.
        """
        success = self.firebase_song_service.delete_song(song_id)

        if not success:
            raise Exception("Failed to delete the song.")

    def get_all_song_ids(self):
        """
        Retrieves all song IDs from Firebase.
        """
        return self.firebase_song_service.get_all_song_ids()
      
    def get_all_songs_with_ids(self):
        return self.firebase_song_service.get_all_songs()
    
    def get_song_count(self):
        return self.firebase_song_service.get_song_count()



    def search_songs(self, query: str):
        """
        Search for songs based on the provided query.
        """
        return self.firebase_song_service.search_songs(query)
