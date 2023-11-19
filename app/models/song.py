from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional


class Song:
    def __init__(self, title: str, duration: int, genre: str, language: str,
                 release_country: str, release_date: Optional[datetime] = None,
                 albums: Optional[List[str]] = None, artists: Optional[List[str]] = None,
                 created_at: Optional[datetime] = None, song_id: Optional[str] = None):
        self.song_id = song_id
        self.title = title
        self.duration = duration
        self.genre = genre
        self.language = language
        self.release_country = release_country
        self.release_date = release_date or datetime.utcnow()
        self.albums = albums or []
        self.artists = artists or []
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self) -> Dict[str, str]:
        """
        Serializes the song object to a dictionary.
        """
        return {
            "title": self.title,
            "duration": self.duration,
            "genre": self.genre,
            "language": self.language,
            "release_country": self.release_country,
            "release_date": (self.release_date + timedelta(hours=3)).isoformat() if self.release_date else None,
            "albums": self.albums,
            "artists": self.artists,
            "created_at": (self.created_at + timedelta(hours=3)).isoformat() if self.created_at else None,
            "song_id": self.song_id
        }

    @staticmethod
    def from_dict(source: Dict) -> 'Song':
        """
        Creates a Song instance from a dictionary.
        """
        song_id = source.get('song_id')
        title = source['title']
        duration = source['duration']
        genre = source['genre']
        language = source['language']
        release_country = source['release_country']

        # Specify Turkey's time zone (UTC+3)
        turkey_time_zone = timezone(timedelta(hours=3))

        release_date_str = source.get('release_date')
        release_date = datetime.strptime(release_date_str, '%Y-%m-%dT%H:%M:%S%z') if release_date_str else None
        release_date = release_date.astimezone(turkey_time_zone) if release_date else None

        albums = source.get('albums', [])
        artists = source.get('artists', [])

        created_at_str = source.get('created_at')
        created_at = datetime.strptime(created_at_str, '%Y-%m-%dT%H:%M:%S%z') if created_at_str else None
        created_at = created_at.astimezone(turkey_time_zone) if created_at else None

        song = Song(title=title, duration=duration, genre=genre, language=language,
                    release_country=release_country, release_date=release_date,
                    albums=albums, artists=artists, created_at=created_at,
                    song_id=song_id)
        return song
