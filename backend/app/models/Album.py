from typing import List
from datetime import datetime

class Album:
    def __init__(self, name: str, imageURL: str, release_date: datetime, total_tracks: int, songs: List[str], artists: List[str]):
        self.name = name
        self.imageURL = imageURL
        self.release_date = release_date
        self.total_tracks = total_tracks
        self.songs = songs
        self.artists = artists

    def to_dict(self) -> dict:
        """
        Serializes the album object to a dictionary suitable for storing in Firestore.
        """
        return {
            "Name": self.name,
            "Image": self.imageURL,
            "Release Date": self.release_date,
            "Total Tracks": self.total_tracks,
            "Songs": self.songs,
            "Artists": self.artists
        }

    @staticmethod
    def from_dict(source: dict) -> 'Album':
        """
        Creates an Album instance from a dictionary, used when retrieving data from Firestore.
        """
        name = source['Name']
        imageURL = source['Image']
        release_date = source['Release Date']
        total_tracks = source['Total Tracks']
        songs = source['Songs']
        artists = source['Artists']

        return Album(name=name, imageURL=imageURL, release_date=release_date, total_tracks=total_tracks, songs=songs, artists=artists)
