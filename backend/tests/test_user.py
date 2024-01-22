import unittest
import json
import sys
import random
sys.path.append("..")
from app import create_app

test_user_data = {
            "username": "testuser" + str(random.randint(0, 100000)),
            "email": f"testuser{str(random.randint(0,10000))}@example.com",
            "password": "A7strongpassword",
        }
test_user_id = None
test_token = None
class UserBlueprintTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test10_signup_user(self):
        response = self.client.post(
            "/user/signup",
            data=json.dumps(test_user_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode())
        self.assertIn("New user created!", data["message"])
        self.assertTrue("user_id" in data)
        global test_user_id
        test_user_id = data["user_id"]

    def test11_login_user(self):
        response = self.client.post(
            "/user/login",
            data=json.dumps(
                {
                    "username_or_email": test_user_data["username"],
                    "password": test_user_data["password"],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertTrue(data["message"] == "User logged in!")

        global test_token
        test_token = data["token"]
        self.client.set_cookie("access_token_cookie", test_token)

    def test12_get_user(self):
        if not test_token or not test_user_id:
            self.fail("No token or user ID available for test.")

        response = self.client.get(
            f"/user/{test_user_id}",

        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertTrue("user" in data)

    def test13_update_user(self):
        if not test_token or not test_user_id:
            self.fail("No token or user ID available for test.")

        response = self.client.put(
            f"/user/{test_user_id}",
            data=json.dumps({"username": "updatedusername"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn("User updated!", data["message"])
    
    def test14_rate_album(self):
        response = self.client.post(
            "/user/rate-album",
            data=json.dumps({"album": "RedKeyImmortalGang", "rate": 5}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test15_unrate_album(self):
        
        response = self.client.post(
            "/user/unrate-album",
            data=json.dumps({"album": "RedKeyImmortalGang"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        
    def test16_get_rated_albums(self):
        response = self.client.get(
            "/user/get-rated-albums",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test17_rate_artist(self):
        response = self.client.post(
            "/user/rate-artist",
            data=json.dumps({"artist": "Drake", "rate": 5}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test18_unrate_artist(self):
        response = self.client.post(
            "/user/unrate-artist",
            data=json.dumps({"artist": "Drake"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test19_get_rated_artists(self):
        response = self.client.get(
            "/user/get-rated-artists",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test20_rate_song(self):
        response = self.client.post(
            "/user/rate-song",
            data=json.dumps({"song": "CAVLIYO", "rate": 5}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test21_unrate_song(self):
        response = self.client.post(
            "/user/unrate-song",
            data=json.dumps({"song": "CAVLIYO"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test22_get_rated_songs(self):
        response = self.client.get(
            "/user/get-rated-songs",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test23_add_playlist(self):
        response = self.client.post(
            "/user/add-playlist",
            data=json.dumps({"playlist_name": "Chill Vibes", "song_names": ["HIRSIZ", "MAHVET"]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

    def test24_add_song_to_playlist(self):
        response = self.client.post(
            "/user/add-song-to-playlist",
            data=json.dumps({"playlist_name": "Chill Vibes", "song_name": "Sustalı"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
    
    
    def test25_delete_song_from_playlist(self):
        response = self.client.delete(
            "/user/delete-song-from-playlist",
            data=json.dumps({"playlist_name": "Chill Vibes", "song_name": "Sustalı"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test26_delete_playlist(self):
        response = self.client.delete(
            "/user/delete-playlist",
            data=json.dumps({"playlist_name": "Chill Vibes"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
    
    def test27_get_all_playlists(self):
        response = self.client.get(
            "/user/get-all-playlists",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test28_add_friend(self):
        if not test_token or not test_user_id:
            self.fail("No token or user ID available for test.")
        response = self.client.post(
            "/user/add-friend",
            data=json.dumps({"friend_username": "asdf"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test29_get_friends(self):
        if not test_token or not test_user_id:
            self.fail("No token or user ID available for test.")
        response = self.client.get(
            "/user/friends",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertTrue("friends" in data)

    def test30_delete_friend(self):
        if not test_token or not test_user_id:
            self.fail("No token or user ID available for test.")
        response = self.client.delete(
            "/user/remove-friend",
            data=json.dumps({"friend_username": "asdf"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test31_subscribe_to_artist(self):
        if not test_token or not test_user_id:
            self.fail("No token or user ID available for test.")
        response = self.client.post(
            "/user/subscriptions/add/O5lRvX18myVaFznej1lE",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test32_get_subscription_list(self):
        response = self.client.get(
            "/user/subscriptions/getAll",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test33_delete_subscription(self):
        response = self.client.delete(
            "/user/subscriptions/delete/O5lRvX18myVaFznej1lE",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test34_search_songs(self):
        response = self.client.get(
            '/user/search?query="Lost"',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)


    ### EDGE CASES ###
    def test35_signup_user_missing_data(self):
        response = self.client.post(
            "/user/signup",
            data=json.dumps({"username": "testuser", "email": "testuser@example.com"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test36_search_songs_no_query(self):
        response = self.client.get(
            "/user/search",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test37_access_protected_route_no_token(self):
        self.client.set_cookie("access_token_cookie", "")
        response = self.client.get(
            f"/user/{test_user_id}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)


    def test38_invalid_token_access(self):
        self.client.set_cookie("access_token_cookie", "invalid_token")
        response = self.client.get(
            f"/user/{test_user_id}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
