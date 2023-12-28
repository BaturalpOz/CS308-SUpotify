from app.utils.firebase_artist_service import FirebaseArtistService
from app.models.Artist import Artist
from typing import List
from app.services.album_service import AlbumService

from app.utils.firebase_album_service import FirebaseAlbumService
from app.utils.firebase_song_service import FirebaseSongService


class ArtistService:
    def __init__(self):
        self.firebase_artist_service = FirebaseArtistService()
        self.firebase_album_service = FirebaseAlbumService()
        self.firebase_song_service = FirebaseSongService()
        self.album_service = AlbumService()
    def create_artist(self, name: str, genres: List[str], image_url: str, popularity: int, albums: List[str]):
        """
        Handles the business logic for creating a new artist.
        """
        if self.firebase_artist_service.get_artist_by_name(name):
            raise ValueError("An artist with that name already exists.")

        new_artist = Artist(name=name, genres=genres, image_url=image_url, popularity=popularity, albums=albums)

       
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
        artist = self.firebase_artist_service.get_artist_by_name(name)     
        return artist if artist else None
        
    def get_all_artists(self):
        return self.firebase_artist_service.get_all_artists()
    
    
    def update_artist(self, artist_id: str, update_data: dict):
        """
        Updates artist information given the artist ID and the new data.
        """
     
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

    def get_artists_from_ids(self,subscription_list:List[str]):
        '''
        Returns the list of artist objects instead of their ids for more usability
        '''
        artist_dict = {}
        artist_list = []
        for sub in subscription_list:
            artist = self.firebase_artist_service.get_artist(sub)
            dict_artist = artist.to_dict()
            dict_artist["Id"] = sub
            artist_list.append(dict_artist)
        artist_dict.update({"subscribed_artists":artist_list})
        return artist_dict
    
    def get_artist_albums(self,artist_id:str):
        '''Gets all album objects belonging to an artist'''
        album_list = []
        artist = self.get_artist_by_id(artist_id)
        albums = artist.albums
        for album in albums:
            album_list.append(self.album_service.get_album_by_name(album))
        return album_list
    
    def get_artist_songs(self,artist_id):
        '''Gets all song objects belonging to an artist'''
        song_list = []
        albums = self.get_artist_albums(artist_id)
        for album in albums:
            dict_album = album.to_dict()
            songs = self.album_service.get_songs_by_names(dict_album["Songs"])
            for song in songs:
                song_list.append(song)
        return song_list
    
    def get_artist_song_ids(self,artist_id:str):
        '''Gets the ids of the songs belonging to an artist'''
        song_ids = []
        artist = self.get_artist_by_id(artist_id)
        for album_name in artist.albums:
            album = self.album_service.get_album_by_name(album_name)
            for song in album.songs:
                song_ids.append(self.firebase_song_service.get_song_id_by_name(song))

        return song_ids