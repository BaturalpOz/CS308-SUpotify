# Models Directory

This directory contains the data models for our Flask application. Each model represents a table in the Firebase database.

## Files

- `user.py` - Defines the User model with all related attributes and methods.
- `artist.py` - Represents the Artist model, containing artist-specific information.
- `album.py` - Defines the Album model, related to the Artist and contains multiple Songs.
- `song.py` - Represents an individual Song, linked to an Album and Artist.
- `playlist.py` - Manages the Playlist model, which can contain many Songs.
