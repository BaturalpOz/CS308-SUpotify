from app.utils.firebase_user_service import FirebaseUserService
from app.utils.firebase_song_service import FirebaseSongService
from app.models.User import User
import random
from datetime import datetime


class UserService:
    def __init__(self):
        self.firebase_user_service = FirebaseUserService()
        self.firebase_song_service = FirebaseSongService()

    def create_user(self, username: str, email: str, password: str):
        """
        Handles the business logic for creating a new user.
        """
        invalid_chars = [".", "#", "$", "[", "]", "/", "@"]
        if self.firebase_user_service.get_user_by_username(username):
            raise ValueError("A user with that username already exists.")
        elif self.firebase_user_service.get_by_email(email):
            raise ValueError("A user with that email already exists.")
        elif any(char in username for char in invalid_chars):
            raise ValueError(
                "Username cannot contain '.', '#', '$', '[', ']', '/', or '@'."
            )

    
        new_user = User(username=username, email=email, raw_password=password)

      
        user_id = self.firebase_user_service.add_user(new_user)

        if user_id:
            return user_id
        else:
            raise Exception("Failed to create a new user in Firebase.")

    def authenticate_user(self, username_or_email: str, password: str):
        """
        Verifies if the provided username and password match a user in the system.
        Returns the user if authenticated, otherwise returns None.
        """
        user = None
        if "@" in username_or_email:
            user = self.firebase_user_service.get_by_email(username_or_email)
        else:
            user = self.firebase_user_service.get_user_by_username(username_or_email)

        if user and User.check_password(user, password):
            return user
        else:
            return None

    def get_user_by_id(self, user_id: str):
        """
        Retrieves a user by their unique user ID.
        """
        if not user_id:
            raise ValueError("User ID cannot be empty.")
        elif not self.firebase_user_service.get_user(user_id):
            raise ValueError("User does not exist.")
        return self.firebase_user_service.get_user(user_id)

    def get_user_by_username(self, username: str):
        """
        Retrieves a user by their unique username.
        """
        if not username:
            raise ValueError("Username cannot be empty.")
        elif not self.firebase_user_service.get_user_by_username(username):
            raise ValueError("User does not exist.")
        return self.firebase_user_service.get_user_by_username(username)

    def update_user(self, user_id: str, update_data: dict):
        """
        Updates user information given the user ID and the new data.
        """
        if "password" in update_data:
       
            update_data["password"] = User.hash_password(update_data["password"])


        success = self.firebase_user_service.update_user(user_id, update_data)

        if not success:
            raise Exception("Failed to update the user.")

    def delete_user(self, user_id: str):
        """
        Deletes a user by their unique user ID.
        """
        return self.firebase_user_service.delete_user(user_id)

    def get_all_user_ids(self):
        """
        Retrieves all user IDs from Firebase.
        """
        return self.firebase_user_service.get_all_user_ids()

    def check_friend_existence(self, user_id: str, friends: list):
        for friend in friends:
            if friend["friendUserID"] == user_id:
                return True
        return False

    def add_friend(self, requester_id: str, friend_username: str):
        requester = self.get_user_by_id(requester_id)
        friend = self.get_user_by_username(friend_username)
        if requester_id == friend.user_id:
            raise ValueError("Cannot add yourself as a friend.")
        elif self.check_friend_existence(friend.user_id, requester.friends):
            raise ValueError("You are already friends with this user.")

        requester.friends.append(
            {
                "friendUsername": friend.username,
                "friendUserID": friend.user_id,
                "includeInRecommendation": friend.settings["includeInRecommendations"],
            }
        )

        self.update_user(requester_id, {"friends": requester.friends})

        return requester.friends

    def remove_friend(self, requester_id: str, friend_username: str):
        requester = self.get_user_by_id(requester_id)
        friend = self.get_user_by_username(friend_username)
        if requester_id == friend.user_id:
            raise ValueError("Cannot remove yourself as a friend.")
        elif not self.check_friend_existence(friend.user_id, requester.friends):
            raise ValueError("You are not friends with this user.")

        requester.friends = [
            friend_iter
            for friend_iter in requester.friends
            if friend.user_id != friend_iter["friendUserID"]
        ]

        self.update_user(requester_id, {"friends": requester.friends})

        return requester.friends

    def get_friends(self, user_id: str):
        user = self.get_user_by_id(user_id)
        return user.friends

    def rate_song(self, user_id: str, song_name: str, rating: int):
        user = self.get_user_by_id(user_id)
        song = self.firebase_song_service.get_song_by_name(song_name)
        rated_song = {
            "artists": song["Artists"],
            "albums": song["Albums"],
            "song": song["Name"],
            "rating": rating,
            "date": f"{datetime.now():%Y-%m-%d %H:%M:%S}"
        }
        user.rated_songs.append(rated_song)
        self.update_user(user_id, {"rated_songs": user.rated_songs})
        return user.rated_songs

    def unrate_song(self, user_id: str, song_name: str):
        user = self.get_user_by_id(user_id)
        song = self.firebase_song_service.get_song_by_name(song_name)
        user.rated_songs = [
            song_iter
            for song_iter in user.rated_songs
            if song["song"] != song_iter["song"]
        ]
        self.update_user(user_id, {"rated_songs": user.rated_songs})
        return user.rated_songs

    def get_rated_songs(self, user_id: str):
        user = self.get_user_by_id(user_id)
        return user.rated_songs

    def rate_artist(self, user_id: str, artist_name: str, rating: int):
        user = self.get_user_by_id(user_id)
        artist = self.firebase_artist_service.get_artist_by_name(artist_name)
        rated_artist = {
            "artist": artist_name,
            "rating": rating,
            "date": f"{datetime.now():%Y-%m-%d %H:%M:%S}"
        }
        user.rated_artists.append(rated_artist)
        self.update_user(user_id, {"rated_artists": user.rated_artists})
        return user.rated_artists
    
    def unrate_artist(self, user_id: str, artist_name: str):
        user = self.get_user_by_id(user_id)
        artist = self.firebase_artist_service.get_artist_by_name(artist_name)
        user.rated_artists = [
            artist_iter
            for artist_iter in user.rated_artists
            if artist["artist"] != artist_iter["artist"]
        ]
        self.update_user(user_id, {"rated_artists": user.rated_artists})
        return user.rated_artists
    
    def get_rated_artists(self, user_id: str):
        user = self.get_user_by_id(user_id)
        return user.rated_artists
    
    def rate_album(self, user_id: str, album_name: str, rating: int):
        user = self.get_user_by_id(user_id)
        album = self.firebase_album_service.get_album_by_name(album_name)
        rated_album = {
            "album": album_name,
            "rating": rating,
            "date": f"{datetime.now():%Y-%m-%d %H:%M:%S}"
        }
        user.rated_albums.append(rated_album)
        self.update_user(user_id, {"rated_albums": user.rated_albums})
        return user.rated_albums
    
    def unrate_album(self, user_id: str, album_name: str):
        user = self.get_user_by_id(user_id)
        album = self.firebase_album_service.get_album_by_name(album_name)
        user.rated_albums = [
            album_iter
            for album_iter in user.rated_albums
            if album["album"] != album_iter["album"]
        ]
        self.update_user(user_id, {"rated_albums": user.rated_albums})
        return user.rated_albums
    
    def get_rated_albums(self, user_id: str):
        user = self.get_user_by_id(user_id)
        return user.rated_albums

    def get_rated_songs_by_date(self, user_id: str, start_date: str, end_date: str):
        user = self.get_user_by_id(user_id)

        to_ret = []
        for song in user.rated_songs:
            album = self.firebase_album_service.get_album_by_name(song["albums"][0])
            album_date = album["Release Date"]
            album_date = album_date.replace(tzinfo=None)

            rating = song["rating"]

            if album_date >= start_date and album_date <= end_date:
                to_ret.append({"song":song, "album_date":album_date})

        return sorted(to_ret, key=lambda x: x["song"]["rating"], reverse=True)[:10]

    def get_rated_albums_by_date(self, user_id: str, start_date: str, end_date: str):
        user = self.get_user_by_id(user_id)

        to_ret = []
        for alb in user.rated_albums:
            album = self.firebase_album_service.get_album_by_name(alb["album"])

            album_date = album["Release Date"]
            album_date = album_date.replace(tzinfo=None)

            rating = alb["rating"]

            if album_date >= start_date and album_date <= end_date:
                to_ret.append({"album":alb, "album_date":album_date, "album_data": album})

        return sorted(to_ret, key=lambda x: x["album"]["rating"], reverse=True)[:10]

    def get_rated_artists_by_date(self, user_id: str, start_date: str, end_date: str):
        user = self.get_user_by_id(user_id)

        to_ret = []
        for artist in user.rated_artists:
            artist_data = self.firebase_artist_service.get_artist_by_name(artist["artist"])
            artist_album = self.firebase_album_service.get_album_by_name(artist_data["Albums"][0])

            album_date = artist_album["Release Date"]
            album_date = album_date.replace(tzinfo=None)

            rating = artist["rating"]

            if album_date >= start_date and album_date <= end_date:
                to_ret.append({"artist":artist, "artist_first_album_date":album_date, "artist_data": artist_data})

        return sorted(to_ret, key=lambda x: x["artist"]["rating"], reverse=True)[:10]

    def get_user_ratings_by_date(self, user_id: str, start_date: str, end_date: str):
        user = self.get_user_by_id(user_id)

        to_ret = []
        for song in user.rated_songs:
            date = song["date"]
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

            rating = song["rating"]

            if date >= start_date and date <= end_date:
                to_ret.append({"song":song, "date":date})

        return sorted(to_ret, key=lambda x: x["song"]["rating"], reverse=True)[:10]

    def get_ratings_for_user(self, user_id: str, type: str):
        user = self.get_user_by_id(user_id)

        to_ret = []
        if type == "songs":
            for song in user.rated_songs:
                to_ret.append({"song":song, "date":datetime.strptime(song["date"], "%Y-%m-%d %H:%M:%S")})

            return sorted(to_ret, key=lambda x: x["song"]["date"], reverse=True)[:10]
        elif type == "albums":
            for album in user.rated_albums:
                to_ret.append({"album":album, "date":datetime.strptime(album["date"], "%Y-%m-%d %H:%M:%S")})

            return sorted(to_ret, key=lambda x: x["album"]["date"], reverse=True)[:10]
        
        elif type == "artists":
            for artist in user.rated_artists:
                to_ret.append({"artist":artist, "date":datetime.strptime(artist["date"], "%Y-%m-%d %H:%M:%S")})

            return sorted(to_ret, key=lambda x: x["artist"]["date"], reverse=True)[:10]
        



    
