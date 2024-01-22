import unittest
import json
import sys
from datetime import datetime

sys.path.append("..")
from app import create_app
test_comment_data = {
    "Commenter": "TestUser",
    "Send_Time": datetime.now().isoformat(),
    "Comment_Content": "This is a test comment."
}
test_comment_id = None
class CommentBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()


    def test1_send_comment(self):
        response = self.client.post(
            "/comment/send",
            data=json.dumps(test_comment_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode())
        global test_comment_id
        test_comment_id = data.get("comment_id")

    def test2_get_comment_by_id(self):
        response = self.client.get(f"/comment/{test_comment_id}")
        self.assertEqual(response.status_code, 200)

    def test3_get_all_comments(self):
        response = self.client.get("/comment/all")
        self.assertEqual(response.status_code, 200)

    ### Error Handling Tests ###

    def test4_send_comment_missing_fields(self):
        incomplete_data = {"Commenter": "IncompleteCommenter"}
        response = self.client.post(
            "/comment/send",
            data=json.dumps(incomplete_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test5_get_nonexistent_comment(self):
        response = self.client.get("/comment/nonexistent_comment_id")
        self.assertEqual(response.status_code, 404)

    def test6_send_invalid_time_format_comment(self):
        invalid_data = test_comment_data.copy()
        invalid_data["Send_Time"] = "invalid_time_format"
        response = self.client.post(
            "/comment/send",
            data=json.dumps(invalid_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 500)


if __name__ == "__main__":
    unittest.main()
