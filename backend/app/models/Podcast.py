from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional

class Episode:
    def __init__(self, name: str, duration_ms: int, description: str):
        self.name = name
        self.duration_ms = duration_ms
        self.description = description
    
    def to_dict(self) -> Dict[str, str]:
        """
        Serializes the episode object to a dictionary.
        """
        return {
            "Name": self.name,
            "Duration": self.duration_ms,
            "Description": self.description
        }
    
    @staticmethod
    def from_dict(source: Dict) -> 'Episode':
        """
        Creates a Episode instance from a dictionary.
        """
        name = source['Name']
        duration_ms = source['Duration']
        description = source['Description']

        return Episode(name=name, duration_ms=duration_ms, description=description)

class Podcast:
    def __init__(self, name: str, episodes: List[Episode] ):
        self.name = name
        self.episodes = episodes

    def to_dict(self) -> Dict[str, str]:
        """
        Serializes the podcast object to a dictionary.
        """
        return {
            "Name": self.name,
            "Episodes": self.episodes
        }

    @staticmethod
    def from_dict(source: Dict) -> 'Podcast':
        """
        Creates a Podcast instance from a dictionary.
        """
        name = source['Name']
        episodes = source['Episodes']

        return Podcast(name=name, episodes=episodes)

