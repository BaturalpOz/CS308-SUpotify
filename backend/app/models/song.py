from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional


class Song:
    def __init__(self, name: str, duration_ms: int, danceability: float, energy: float, loudness: float, tempo: float, albums: List[str], artists: List[str]):
        self.name = name
        self.duration_ms = duration_ms
        self.danceability = danceability
        self.energy = energy
        self.loudness = loudness
        self.tempo = tempo
        self.albums = albums
        self.artists = artists

    def to_dict(self) -> Dict[str, str]:
        """
        Serializes the song object to a dictionary.
        """
        return {
            "Name": self.name,
            "Duration": self.duration_ms,
            "Danceability": self.danceability,
            "Energy": self.energy,
            "Loudness": self.loudness,
            "Tempo": self.tempo,
            "Albums": self.albums,
            "Artists": self.artists
        }

    @staticmethod
    def from_dict(source: Dict) -> 'Song':
        """
        Creates a Song instance from a dictionary.
        """
        name = source['Name']
        duration_ms = source['Duration']
        danceability = source['Danceability']
        energy = source['Energy']
        loudness = source['Loudness']
        tempo = source['Tempo']
        albums = source['Albums']
        artists = source['Artists']

        return Song(name=name, duration_ms=duration_ms, danceability=danceability, energy=energy, loudness=loudness, tempo=tempo, albums=albums, artists=artists)
   

