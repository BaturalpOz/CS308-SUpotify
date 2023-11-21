from app.utils.firebase_user_service import FirebaseUserService
from app.models.User import User
import random

class UserService:
    def __init__(self):
        self.firebase_user_service = FirebaseUserService()

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

        # Create a new User instance
        new_user = User(username=username, email=email, raw_password=password)

        # Add the new user to Firebase, which returns the user_id if successful
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
            # If updating password, hash the new password before updating
            update_data["password"] = User.hash_password(update_data["password"])

        # Update the user in Firebase
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
        
        requester.friends.append({"friendUserID": friend.user_id, "includeInRecommendation": random.choice([True, False])})
        
        self.update_user(requester_id, {"friends": requester.friends})

        return requester.friends

    def remove_friend(self, requester_id: str, friend_username: str):
        requester = self.get_user_by_id(requester_id)
        friend = self.get_user_by_username(friend_username)
        if requester_id == friend.user_id:
            raise ValueError("Cannot remove yourself as a friend.")
        elif not self.check_friend_existence(friend.user_id, requester.friends):
            raise ValueError("You are not friends with this user.")

        requester.friends = [friend_iter for friend_iter in requester.friends if friend.user_id != friend_iter["friendUserID"]]
        
        self.update_user(requester_id, {"friends": requester.friends})

        return requester.friends
    
    def get_friends(self, user_id: str):
        user = self.get_user_by_id(user_id)
        return user.friends
    
