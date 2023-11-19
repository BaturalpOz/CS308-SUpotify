from app.utils.firebase_song_service import FirebaseSongService
from app.models.song import Song
from datetime import datetime


class SongService:
    def __init__(self):
        self.firebase_song_service = FirebaseSongService()

    def add_song(self, title: str, duration: int, genre: str, language: str,
                 release_country: str, release_date: datetime, albums: list, artists: list):
        """
        Handles the business logic for adding a new song.
        """
        # Create a new Song instance
        new_song = Song(
            title=title,
            duration=duration,
            genre=genre,
            language=language,
            release_country=release_country,
            release_date=release_date,
            albums=albums,
            artists=artists
        )

        # Add the new song to Firebase, which returns the song_id if successful
        song_id = self.firebase_song_service.add_song(new_song)

        if song_id:
            return song_id
        else:
            raise Exception("Failed to add a new song in Firebase.")

    def get_song_by_id(self, song_id: str):
        """
        Retrieves a song by its unique song ID.
        """
        return self.firebase_song_service.get_song_by_id(song_id)

    def update_song(self, song_id: str, update_data: dict):
        """
        Updates song information given the song ID and the new data.
        """
        # Update the song in Firebase
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
