from typing import List
from datetime import datetime

class Album:
    def __init__(self, name: str, imageURL: str, language: str, country: str, release_date: datetime, songs: List[str], title: str):
        self.name = name
        self.imageURL = imageURL
        self.language = language
        self.country = country
        self.release_date = release_date
        self.songs = songs
        self.title = title

    def to_dict(self) -> dict:
        """
        Serializes the album object to a dictionary suitable for storing in Firestore.
        """
        return {
            "Name": self.name,
            "Image": self.imageURL,
            "Languages": self.language,
            "Release Country": self.country,
            "Release Date": self.release_date, #.isoformat(),
            "Songs": self.songs,
            "Title": self.title
        }

    @staticmethod
    def from_dict(source: dict) -> 'Album':
        """
        Creates an Album instance from a dictionary, used when retrieving data from Firestore.
        """
        name = source['Name']
        imageURL = source['Image']
        language = source['Languages']
        country = source['Release Country']
        release_date = source['Release Date'] #datetime.fromisoformat(source['Release Date'].strftime('%Y-%m-%dT%H:%M:%Ss'))
        songs = source['Songs']
        title = source['Title']

        return Album(name=name, imageURL=imageURL, language=language, country=country, release_date=release_date, songs=songs, title=title)
