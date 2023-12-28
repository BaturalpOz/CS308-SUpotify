from app.utils.firebase_comment_service import FirebaseCommentService
from app.models.Comment import Comment
from datetime import datetime
from typing import Optional, List


class CommentService:
    def __init__(self):
        self.firebase_comment_service = FirebaseCommentService()

    def send_comment(self, commenter_name: str, comment_content: str, commented_at: Optional[datetime] = None):
        """
        Handles the business logic for adding a new comment.
        """
        if commented_at is None:
            commented_at = datetime.now()

        new_comment = Comment(
            commenter_name=commenter_name,
            comment_content=comment_content,
            commented_at=commented_at  # Convert to timestamp
        )

        comment_id = self.firebase_comment_service.send_comment(new_comment)

        if comment_id:
            return comment_id
        else:
            raise ValueError("Failed to add a new comment in Firebase.")

    def get_comment(self, comment_id: str):
        """
        Retrieves a comment by its unique comment ID.
        """
        if not comment_id:
            raise ValueError("comment ID cannot be empty.")

        comment = self.firebase_comment_service.get_comment(comment_id)

        if not comment:
            print(f"Comment with ID {comment_id} does not exist.")
            raise ValueError("comment does not exist.")

        print(f"Retrieved comment: {comment.to_dict()}")
        return comment

    def get_all_comment_ids(self) -> Optional[List[str]]:
        """
        Retrieves all comment IDs from Firebase.
        """
        return self.firebase_comment_service.get_all_comment_ids()
