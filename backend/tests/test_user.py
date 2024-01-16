import unittest
import json
import sys

sys.path.append("..")
from app import create_app

class UserBlueprintTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.test_user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "A7strongpassword",
        }
        self.test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNE45WWQ2cE8zckE2d1VYa3lISFgiLCJleHAiOjE3MDM2MTU1NjR9.DfToqVXbwexrXpYvHCV0jd5d5OmCdt97Rd8SJypiFNc"
        self.test_user_id = None

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test10_signup_user(self):
        response = self.client.post(
            "/user/signup",
            data=json.dumps(self.test_user_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode())
        self.assertIn("New user created!", data["message"])
        self.assertTrue("user_id" in data)

        self.test_user_id = data["user_id"]
        print(self.test_user_id)

    def test11_login_user(self):
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

        self.test_token = data["token"]

    def test12_get_user(self):
        print(self.test_token)
        print(self.test_user_id)
        if not self.test_token or not self.test_user_id:
            self.fail("No token or user ID available for test.")

        response = self.client.get(
            f"/user/{self.test_user_id}",
            headers={"Cookie": self.test_token},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertTrue("user" in data)

    def test13_update_user(self):
        if not self.test_token or not self.test_user_id:
            self.fail("No token or user ID available for test.")

        response = self.client.put(
            f"/user/{self.test_user_id}",
            headers={"Cookie": self.test_token},
            data=json.dumps({"username": "updatedusername"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn("User updated!", data["message"])
    
    def test14_rate_album(self):
        response = self.client.post(
            "/user/rate-album",
            headers={"Cookie": self.test_token},
            data=json.dumps({"album": "RedKeyImmortalGang", "rate": 5}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test15_unrate_album(self):
        response = self.client.post(
            "/user/unrate-album",
            headers={"Cookie": self.test_token},
            data=json.dumps({"album": "RedKeyImmortalGang"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        
    def test16_get_rated_albums(self):
        response = self.client.get(
            "/user/get-rated-albums",
            headers={"Cookie": self.test_token},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test17_rate_artist(self):
        response = self.client.post(
            "/user/rate-artist",
            headers={"Cookie": self.test_token},
            data=json.dumps({"artist": "Drake", "rate": 5}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test18_unrate_artist(self):
        response = self.client.post(
            "/user/unrate-artist",
            headers={"Cookie": self.test_token},
            data=json.dumps({"artist": "Drake"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test19_get_rated_artists(self):
        response = self.client.get(
            "/user/get-rated-artists",
            headers={"Cookie": self.test_token},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test20_rate_song(self):
        response = self.client.post(
            "/user/rate-song",
            headers={"Cookie": self.test_token},
            data=json.dumps({"song": "CAVLIYO", "rating": 5}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test21_unrate_song(self):
        response = self.client.post(
            "/user/unrate-song",
            headers={"Cookie": self.test_token},
            data=json.dumps({"song": "CAVLIYO"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test22_get_rated_songs(self):
        response = self.client.get(
            "/user/get-rated-songs",
            headers={"Cookie": self.test_token},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test23_add_playlist(self):
        response = self.client.post(
            "/user/add-playlist",
            headers={"Cookie": self.test_token},
            data=json.dumps({"playlist_name": "Chill Vibes", "song_names": ["Song1", "Song2"]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

    def test24_delete_playlist(self):
        response = self.client.delete(
            "/user/delete-playlist",
            headers={"Cookie": self.test_token},
            data=json.dumps({"playlist_name": "Chill Vibes"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test25_add_song_to_playlist(self):
        response = self.client.post(
            "/user/add-song-to-playlist",
            headers={"Cookie": self.test_token},
            data=json.dumps({"playlist_name": "Chill Vibes", "song_name": "Song3"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

    def test26_delete_song_from_playlist(self):
        response = self.client.delete(
            "/user/delete-song-from-playlist",
            headers={"Cookie": self.test_token},
            data=json.dumps({"playlist_name": "Chill Vibes", "song_name": "Song3"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test27_get_all_playlists(self):
        response = self.client.get(
            "/user/get-all-playlists",
            headers={"Cookie": self.test_token},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test28_add_friend(self):
        if not self.test_token or not self.test_user_id:
            self.fail("No token or user ID available for test.")
        response = self.client.post(
            "/user/add-friend",
            headers={"Cookie": self.test_token},
            data=json.dumps({"friend_username": "asdf"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test29_get_friends(self):
        if not self.test_token or not self.test_user_id:
            self.fail("No token or user ID available for test.")
        response = self.client.get(
            "/user/friends",
            headers={"Cookie": self.test_token},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertTrue("friends" in data)

    def test30_delete_friend(self):
        if not self.test_token or not self.test_user_id:
            self.fail("No token or user ID available for test.")
        response = self.client.delete(
            "/user/remove-friend",
            headers={"Cookie": self.test_token},
            data=json.dumps({"friend_username": "asdf"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test31_subscribe_to_artist(self):
        response = self.client.post(
            "/subscriptions/add/O5lRvX18myVaFznej1lE",
            headers={"Cookie": self.test_token},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test34_get_subscription_list(self):
        response = self.client.get(
            "/subscriptions/getAll",
            headers={"Cookie": self.test_token},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test35_delete_subscription(self):
        response = self.client.delete(
            "/subscriptions/delete/O5lRvX18myVaFznej1lE",
            headers={"Cookie": self.test_token},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test36_search_songs(self):
        response = self.client.get(
            '/search?query="Lost"',
            headers={"Cookie": self.test_token},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test37_logout_user(self):
        if not self.test_token or not self.test_user_id:
            self.fail("No token or user ID available for test.")

        response = self.client.post(
            "/user/logout",
            headers={"Cookie": self.test_token},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn("User logged out!", data["message"])

    def test38_delete_user(self):
        if not self.test_token or not self.test_user_id:
            self.fail("No token or user ID available for test.")

        response = self.client.delete(
            f"/user/{self.test_user_id}",
            headers={"Cookie": self.test_token},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn("User deleted!", data["message"])

    ### EDGE CASES ###
    def test39_signup_user_missing_data(self):
        response = self.client.post(
            "/user/signup",
            data=json.dumps({"username": "testuser", "email": "testuser@example.com"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test40_invalid_token_access(self):
        response = self.client.get(
            f"/user/{self.test_user_id}",
            headers={"Cookie": "invalid_token"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test41_search_songs_no_query(self):
        response = self.client.get(
            "/user/search",
            headers={"Cookie": self.test_token},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test42_access_protected_route_no_token(self):
        response = self.client.get(
            f"/user/{self.test_user_id}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test43_access_protected_route_invalid_token(self):
        response = self.client.get(
            f"/user/{self.test_user_id}",
            headers={"Cookie": "invalid_token"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
