from datetime import datetime
from app.utils.firebase_album_service import FirebaseAlbumService
from app.models.Album import Album
from typing import List
from app.models.Song import Song

from app.services.song_service import SongService

class AlbumService:
    def __init__(self):
        self.firebase_album_service = FirebaseAlbumService()
        self.song_service = SongService()

    def create_album(self, name: str, imageURL: str, release_date: datetime, total_tracks: int, songs: List[str], artists: List[str]):
        """
        Handles the business logic for creating a new album.
        """
        if self.firebase_album_service.get_album_by_name(name):
            raise ValueError("An album with that name already exists.")

        # Create a new Album instance
        new_album = Album(name=name, imageURL=imageURL, release_date=release_date, total_tracks=total_tracks, songs=songs, artists=artists)

        # Add the new album to Firebase, which returns the album_id if successful
        album_id = self.firebase_album_service.add_album(new_album)

        if album_id:
            return album_id
        else:
            raise Exception("Failed to create a new album in Firebase.")

    def get_album_by_id(self, album_id: str):
        """
        Retrieves an album by its unique album ID.
        """
        if not album_id:
            raise ValueError("Album ID cannot be empty.")
        elif not self.firebase_album_service.get_album(album_id):
            raise ValueError("Album does not exist.")
        return self.firebase_album_service.get_album(album_id)

    def get_album_by_name(self, name: str):
        """
        Retrieves an album by its unique name.
        """
        if not name:
            raise ValueError("Name cannot be empty.")
        elif not self.firebase_album_service.get_album_by_name(name):
            raise ValueError("Album does not exist.")
        return self.firebase_album_service.get_album_by_name(name)

    def update_album(self, album_id: str, update_data: dict):
        """
        Updates album information given the album ID and the new data.
        """
        # Update the album in Firebase
        success = self.firebase_album_service.update_album(album_id, update_data)

        if not success:
            raise Exception("Failed to update the album.")

   

    def get_all_album_ids(self):
        """
        Retrieves all album IDs from Firebase.
        """
        return self.firebase_album_service.get_all_album_ids()
    def delete_album(self, album_id: str):
        """
        Deletes an album by its unique album ID.
        """
        self.firebase_album_service.delete_album(album_id)

    def get_songs_by_ids(self,album_id:str):
        song_list = []
        album = self.get_album_by_id(album_id)
        songs = album.songs
        for song in songs:
            song_list.append(self.song_service.get_song_by_id(song))
        return song_list
    
    def get_songs_by_names(self,names:List[str]):
        song_list = []
        for name in names:
            song = self.song_service.get_song_by_name(name)
            song_list.append(song)
        return song_list
