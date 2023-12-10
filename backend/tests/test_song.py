import unittest
import json
from app import create_app
from datetime import datetime


class SongBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.song_id = "None"  # Store the song ID for later use

    def test1_add_song(self):
        song_data = {
            "title": "Song Titleee",
            "duration": 240,
            "genre": "Electronic",
            "language": "English",
            "release_country": "India",
            "release_date": "2023-11-15T12:00:00Z",
            "albums": ["album13"],
            "artists": ["artist14", "artist15"],
        }
        response = self.client.post(
            "/song/songs",
            data=json.dumps(song_data),
            content_type="application/json",
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn("New song created!", data["message"])
        self.assertTrue("song_id" in data)
        self.song_id = data["song_id"]  # Store the song ID

def test2_get_song(self):
    if not self.song_id:
        self.fail("No song ID available for test.")
    response = self.client.get(f"/song/songs/{self.song_id}")
    data = json.loads(response.data.decode())
    if response.status_code == 200:
        self.assertTrue("song" in data)
    elif response.status_code == 404:
        self.assertIn("Song not found", data["message"])

def test3_get_all_songs(self):
    if not self.song_id:
        self.fail("No song ID available for test.")
    response = self.client.get("/song/all")
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.data.decode())
    self.assertTrue("song_ids" in data)

def test4_get_song_by_name(self):
    if not self.song_id:
        self.fail("No song ID available for test.")
    response = self.client.get(f"/song/get_by_name/{self.test2_get_song['Name']}")
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.data.decode())
    self.assertTrue("song" in data)


    def test5_update_song(self):
        song_id = "78Un1CEzUONSvewAA9Lz"
        update_data = {"duration": 300}
        response = self.client.put(
            f"/song/songs/{song_id}",
            data=json.dumps(update_data),
            content_type="application/json",
        )
        data = json.loads(response.data.decode())
        if response.status_code == 200:
            self.assertIn("Song updated!", data["message"])
        elif response.status_code == 404:
            self.assertIn("Song not found", data["message"])

    def test6_delete_song(self):
        song_id = "qWHRVo4dW9x78ss8tGbk"  # Replace with an existing or non-existent song ID in your test environment
        response = self.client.delete(f"/song/songs/{song_id}")
        data = json.loads(response.data.decode())

        if response.status_code == 200:
            self.assertIn("Song deleted!", data["message"])
        elif response.status_code == 404:
            self.assertIn("Song not found", data["message"])
        else:
            # Check for unexpected status codes
            self.fail(f"Unexpected status code: {response.status_code}, Message: {data['message']}")


if __name__ == "__main__":
    unittest.main()
