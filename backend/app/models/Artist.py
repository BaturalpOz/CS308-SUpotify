from typing import List, Dict, Optional


class Artist:
    def __init__(self, name: str, genres: List[str], image_url: str, popularity: int, albums: List[str]):
        self.name = name
        self.genres = genres
        self.image_url = image_url
        self.popularity = popularity
        self.albums = albums

    def to_dict(self) -> Dict:
        """
        Serializes the artist object to a dictionary suitable for storing in Firestore.
        """
        return {
            "Name": self.name,
            "Genres": self.genres,
            "Image": self.image_url,
            "Popularity": self.popularity,
            "Albums": self.albums
        }

    @staticmethod
    def from_dict(source: Dict) -> 'Artist':
        """
        Creates an Artist instance from a dictionary, used when retrieving data from Firestore.
        """
        if not all(key in source for key in ('Name', 'Genres', 'Image', 'Popularity', 'Albums')):
            raise KeyError("Missing required field in the document")

        name = source['Name']
        genres = source['Genres']
        image_url = source['Image']
        popularity = source['Popularity']
        albums = source['Albums']

        return Artist(name=name, genres=genres, image_url=image_url, popularity=popularity, albums=albums)

