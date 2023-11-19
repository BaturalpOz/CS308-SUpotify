from app.utils.firebase_artist_service import FirebaseArtistService
from app.models.Artist import Artist


class ArtistService:
    def __init__(self):
        self.firebase_artist_service = FirebaseArtistService()

    def create_artist(self, name: str, description: str, image_url: str,albums):
        """
        Handles the business logic for creating a new artist.
        """
        if self.firebase_artist_service.get_artist_by_name(name):
            raise ValueError("An artist with that name already exists.")

        # Create a new Artist instance
        new_artist = Artist(name=name, description=description, image_url=image_url,albums=albums)

        # Add the new artist to Firebase, which returns the artist_id if successful
        artist_id = self.firebase_artist_service.add_artist(new_artist)

        if artist_id:
            return artist_id
        else:
            raise Exception("Failed to create a new artist in Firebase.")

    def get_artist_by_id(self, artist_id: str):
        """
        Retrieves an artist by their unique artist ID.
        """
        if not artist_id:
            raise ValueError("Artist ID cannot be empty.")
        elif not self.firebase_artist_service.get_artist(artist_id):
            raise ValueError("Artist does not exist.")
        return self.firebase_artist_service.get_artist(artist_id)

    def get_artist_by_name(self, name: str):
        """
        Retrieves an artist by their unique name.
        """
        if not name:
            raise ValueError("Name cannot be empty.")
        elif not self.firebase_artist_service.get_artist_by_name(name):
            raise ValueError("Artist does not exist.")
        return self.firebase_artist_service.get_artist_by_name(name)

    def update_artist(self, artist_id: str, update_data: dict):
        """
        Updates artist information given the artist ID and the new data.
        """
        # Update the artist in Firebase
        success = self.firebase_artist_service.update_artist(artist_id, update_data)

        if not success:
            raise Exception("Failed to update the artist.")

    def delete_artist(self, artist_id: str):
        """
        Deletes an artist by their unique artist ID.
        """
        return self.firebase_artist_service.delete_artist(artist_id)

    def get_all_artist_ids(self):
        """
        Retrieves all artist IDs from Firebase.
        """
        return self.firebase_artist_service.get_all_artist_ids()
