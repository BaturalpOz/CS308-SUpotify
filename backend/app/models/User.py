import bcrypt
from datetime import datetime
from typing import List, Dict, Optional, Union


class User:
    def __init__(
        self,
        username: str,
        email: str,
        raw_password: str,
        user_id: Optional[str] = None,
        settings: Optional[Dict[str, str]] = None,
        created_at: Optional[datetime] = None,
        last_login: Optional[datetime] = None,
        friends: Optional[List[Dict[str, str]]] = None,
        rated_songs: Optional[List[Dict[str, str]]] = None,
        rated_artists: Optional[List[str]] = None,
        rated_albums: Optional[List[str]] = None,
        playlists: Optional[List[Dict[str, Union[str, List[str]]]]] = None,
        subscribed_artists: Optional[List[str]] = None
    ):
        """
        Creates a new user object.
        """
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = self.hash_password(
            raw_password
        )  # Hash the password before storing
        self.settings = settings if settings else {"includeInRecommendations": True}
        self.created_at = created_at if created_at else datetime.utcnow()
        self.last_login = last_login if last_login else datetime.utcnow()
        self.friends = friends if friends else []
        self.rated_songs = rated_songs if rated_songs else []
        self.rated_artists = rated_artists if rated_artists else []
        self.rated_albums = rated_albums if rated_albums else []
        self.playlists = playlists if playlists else[]
        self.subscribed_artists = subscribed_artists if subscribed_artists else[]
    @staticmethod
    def hash_password(raw_password: str) -> bytes:
        """
        Hashes the password using bcrypt.
        """
        return bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt())

    def check_password(self, raw_password: str) -> bool:
        """
        Checks the provided password against the hashed one in the database.
        """
        return bcrypt.checkpw(raw_password.encode("utf-8"), self.password)

    def to_dict(self) -> Dict:
        """
        Serializes the user object to a dictionary suitable for storing in Firestore.
        """
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password.decode("utf-8"),  # Store as a string in Firestore
            "User_Settings": self.settings,
            "createdAt": self.created_at.isoformat(),  # Convert datetime to string
            "lastLogin": self.last_login.isoformat(),  # Convert datetime to string
            "friends": [
                {
                    "friendUsername": friend["friendUsername"],
                    "friendUserID": friend["friendUserID"],
                    "includeInRecommendation": friend["includeInRecommendations"],
                }
                for friend in self.friends
            ]
            if self.friends
            else [],
            "rated_songs": self.rated_songs if self.rated_songs else [],
            "rated_artists": self.rated_artists if self.rated_artists else [],
            "rated_albums": self.rated_albums if self.rated_albums else [],
            "playlists": self.playlists if self.playlists else[],
            "subscribed_artists":self.subscribed_artists if self.subscribed_artists else[]
        }

    @staticmethod
    def from_dict(source: Dict) -> "User":
        """
        Creates a User instance from a dictionary, used when retrieving data from Firestore.
        """
        if not all(key in source for key in ("username", "email", "password")):
            raise KeyError("Missing required field in the document")

        user_id = source.get("user_id")
        username = source["username"]
        email = source["email"]
        password = source["password"]
        settings = source.get("User_Settings", {"includeInRecommendations": True})
        created_at = (
            datetime.fromisoformat(source.get("createdAt"))
            if source.get("createdAt")
            else datetime.utcnow()
        )
        last_login = (
            datetime.fromisoformat(source.get("lastLogin"))
            if source.get("lastLogin")
            else datetime.utcnow()
        )
        friends = source.get("friends", [])
        rated_songs = source.get("rated_songs", [])
        rated_artists = source.get("rated_artists", [])
        rated_albums = source.get("rated_albums", [])
        playlists = source.get("playlists", [])
        subscribed_artists = source.get("subscribed_artists",[])
        user = User(
            username=username,
            email=email,
            raw_password=password,
            user_id=user_id,
            settings=settings,
            created_at=created_at,
            last_login=last_login,
            friends=friends,
            rated_songs=rated_songs,
            rated_artists=rated_artists,
            rated_albums=rated_albums,
            playlists=playlists,
            subscribed_artists=subscribed_artists
        )
        user.password = password.encode("utf-8")  # Ensure the password is in bytes
        return user
