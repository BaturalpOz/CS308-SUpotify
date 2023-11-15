import unittest
import json
import sys 

sys.path.append("..")
from app import create_app


class UserBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_signup_user(self):
        user_data = {
            "username": "userzero",
            "email": "userzero@somewhere.com",
            "password": "youcannotdecodethispassword",
        }
        response = self.client.post(
            "/user/signup", data=json.dumps(user_data), content_type="application/json"
        )
        print(response.data)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)
        self.assertIn("New user created!", data["message"])
        self.assertTrue("user_id" in data)

    def test_login_user(self):
        print("Testing with login using username")
        user_data = {
            "username_or_email": "userzero1",
            "password": "youcannotdecodethispassword",
        }
        response = self.client.post(
            "/user/login", data=json.dumps(user_data), content_type="application/json"
        )
        print(response.data)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue("token" in data)

        print("Testing with login using email")
        user_data = {
            "username_or_email": "userzero1@somewhere.com",
            "password": "youcannotdecodethispassword",
        }

        response = self.client.post(
            "/user/login", data=json.dumps(user_data), content_type="application/json"
        )
        print(response.data)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue("token" in data)

    def test_get_user(self):
        user_data = {
            "user_id": "hJctCX3bKece5MaAa37B"
        }
        response = self.client.get(
            "/user", data=json.dumps(user_data), content_type="application/json"
        )
        print(response.data)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue("user" in data)

if __name__ == "__main__":
    unittest.main()
