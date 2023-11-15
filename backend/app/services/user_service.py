from app.utils.firebase_user_service import FirebaseUserService
from app.models.user import User

class UserService:
    def __init__(self):
        self.firebase_user_service = FirebaseUserService()

    def create_user(self, username: str, email: str, password: str):
        """
        Handles the business logic for creating a new user.
        """
        invalid_chars = ['.', '#', '$', '[', ']', '/', '@']
        if self.firebase_user_service.get_user_by_username(username):
            raise ValueError("A user with that username already exists.")
        elif self.firebase_user_service.get_by_email(email):
            raise ValueError("A user with that email already exists.")
        elif any(char in username for char in invalid_chars):
            raise ValueError("Username cannot contain '.', '#', '$', '[', ']', '/', or '@'.")

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
        """
        if '@' in username_or_email:
            user = self.firebase_user_service.get_by_email(username_or_email)
        else:
            user = self.firebase_user_service.get_user_by_username(username_or_email)
        
        if user and User.check_password(user, password):
            return user
        else:
            raise ValueError("Invalid username or password.")

    def get_user_by_id(self, user_id: str):
        """
        Retrieves a user by their unique user ID.
        """
        return self.firebase_user_service.get_user(user_id)

    def update_user(self, user_id: str, update_data: dict):
        """
        Updates user information given the user ID and the new data.
        """
        if 'password' in update_data:
            # If updating password, hash the new password before updating
            update_data['password'] = User.hash_password(update_data['password'])
            
        # Update the user in Firebase
        success = self.firebase_user_service.update_user(user_id, update_data)
        
        if not success:
            raise Exception("Failed to update the user.")

    def delete_user(self, user_id: str):
        """
        Deletes a user by their unique user ID.
        """
        return self.firebase_user_service.delete_user(user_id)
    