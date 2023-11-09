from datetime import datetime
from typing import List
class Song:
    class Like:
        user: str  # Only contains the user ID instead of storing the user model.
        like_time: datetime
    class Comment:
        comment: str
        rating: int
        user: str  # Only contains the user ID instead of storing the user model.
        time_stamp: datetime
    albums: List[str]
    artists: List[str]
    createdat: datetime
    duration: int  # Duration in seconds
    genre: str
    language: str
    release_country: str
    release_date: datetime
    title: str
    likes:List[Like]
    comments:List[Comment]
   

