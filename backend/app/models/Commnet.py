from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional


class Comment:
    def __init__(self, commenter_name: str, comment_content: str, commented_at: Optional[datetime] = None):
        self.commenter_name = commenter_name
        self.commented_at = commented_at
        self.comment_content = comment_content

    def to_dict(self) -> Dict[str, str]:
        """
        Serializes the comment object to a dictionary.
        """
        return {
            "Commenter": self.commenter_name,
            "Send_Time": self.commented_at.isoformat() if self.commented_at else None,
            "Comment": self.comment_content
        }

    @staticmethod
    def from_dict(source: Dict) -> 'Comment':
        """
        Creates a Comment instance from a dictionary.
        """
        commenter_name = source['Commenter']
        commented_at_str = source['Send_Time']
        comment_content = source['Comment']

        commented_at = datetime.fromisoformat(commented_at_str) if commented_at_str else None

        return Comment(commenter_name=commenter_name, commented_at=commented_at, comment_content=comment_content)
