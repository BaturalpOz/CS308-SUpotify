from typing import List, Dict, Optional


class Artist:
    def __init__(self, name: str, description: str, image_url: str, albums: Optional[List[str]] = None):
        self.name = name
        self.description = description
        self.image_url = image_url
        self.albums = albums if albums else []

    def to_dict(self) -> Dict:
        """
        Serializes the artist object to a dictionary suitable for storing in Firestore.
        """
         #str_albums = []
         #if(len(self.albums) > 0):
           #  for album_index in range(len(self.albums)):
            #     str_albums[album_index] = self.albums[album_index].path

        return {
            "Name": self.name,
            "Description": self.description,
            "Image": self.image_url,
            "Albums": self.albums
        }

    @staticmethod
    def from_dict(source: Dict) -> 'Artist':
        """
        Creates an Artist instance from a dictionary, used when retrieving data from Firestore.
        """
        if not all(key in source for key in ('Name', 'Description', 'Image')):
            raise KeyError("Missing required field in the document")

        name = source['Name']
        description = source['Description']
        image_url = source['Image']
        albums = source["Albums"]

        return Artist(name=name, description=description, image_url=image_url, albums=albums)
