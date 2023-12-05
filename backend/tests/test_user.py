import unittest
import json
import sys

sys.path.append("..")
from app import create_app

test_token = None
test_user_id = None
class UserBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        self.test_user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "A7strongpassword",
        }

    def test1_signup_user(self):
        global test_user_id

        response = self.client.post(
            "/user/signup",
            data=json.dumps(self.test_user_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode())
        self.assertIn("New user created!", data["message"])
        self.assertTrue("user_id" in data)

        test_user_id = data["user_id"]

    def test2_login_user(self):
        global test_token
        response = self.client.post(
            "/user/login",
            data=json.dumps(
                {
                    "username_or_email": self.test_user_data["username"],
                    "password": self.test_user_data["password"],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertTrue(data["message"] == "User logged in!")

        test_token = data["token"]

    def test3_get_user(self):
        if not test_token or not test_user_id:
            self.fail("No token or user ID available for test.")

        response = self.client.get(
            f"/user/{test_user_id}",
            headers={"Cookie": test_token},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertTrue("user" in data)

    def test4_update_user(self):
        if not test_token or not test_user_id:
            self.fail("No token or user ID available for test.")

        response = self.client.put(
            f"/user/{test_user_id}",
            headers={"Cookie": test_token},
            data=json.dumps({"username": "updatedusername"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn("User updated!", data["message"])

    def test5_delete_user(self):
        if not test_token or not test_user_id:
            self.fail("No token or user ID available for test.")

        response = self.client.delete(
            f"/user/{test_user_id}",
            headers={"Cookie": test_token},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn("User deleted!", data["message"])

if __name__ == "__main__":
    unittest.main()
