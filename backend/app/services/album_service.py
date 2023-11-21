from datetime import datetime
from app.utils.firebase_album_service import FirebaseAlbumService
from app.models.Album import Album
from typing import List

class AlbumService:
    def __init__(self):
        self.firebase_album_service = FirebaseAlbumService()

    def create_album(self, name: str, imageURL: str, language: str, country: str, release_date: datetime, songs: List[str], title: str):
        """
        Handles the business logic for creating a new album.
        """
        if self.firebase_album_service.get_album_by_name(name):
            raise ValueError("An album with that name already exists.")

        # Create a new Album instance
        new_album = Album(name=name, imageURL=imageURL, language=language, country=country, release_date=release_date, songs=songs, title=title)

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


