import unittest
import json
import sys 
sys.path.append("..")
from app import create_app
from datetime import datetime


song_id = None
class SongBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test10_add_song(self):
        song_data = {
            "Name": "New Song",
            "Duration": 210000,
            "Danceability": 0.75,
            "Energy": 0.8,
            "Loudness": -5.5,
            "Tempo": 120,
            "Albums": ["Album1"],
            "Artists": ["Artist1"]
        }
        response = self.client.post(
            "/song/songs",
            data=json.dumps(song_data),
            content_type="application/json",
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn("New song created!", data["message"])
        global song_id
        song_id = data.get("song_id")

    def test11_get_song(self):
        if not song_id:
            self.fail("No song ID available for test.")
        response = self.client.get(f"/song/{song_id}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn("song", data)

    def test12_get_all_songs(self):
        response = self.client.get("/song/all")
        self.assertEqual(response.status_code, 200)

    def test13_get_song_by_name(self):
        response = self.client.get("/song/get_by_name/New Song")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn("song", data)

    def test14_update_song(self):
        if not song_id:
            self.fail("No song ID available for test.")
        update_data = {"Name": "Updated Song"}
        response = self.client.put(
            f"/song/songs/{song_id}",
            data=json.dumps(update_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn("Song updated!", data["message"])

    def test15_delete_song(self):
        if not song_id:
            self.fail("No song ID available for test.")
        response = self.client.delete(f"/song/songs/{song_id}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn("Song deleted!", data["message"])

    ### Error Handling Tests ###

    def test16_add_song_missing_fields(self):
        song_data = {
            "Name": "Incomplete Song",
            # Missing other fields
        }
        response = self.client.post(
            "/song/songs",
            data=json.dumps(song_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test17_get_nonexistent_song(self):
        response = self.client.get("/song/nonexistent_song_id")
        self.assertEqual(response.status_code, 404)

    def test18_update_nonexistent_song(self):
        update_data = {"Name": "Nonexistent Song"}
        response = self.client.put(
            "/song/songs/nonexistent_song_id",
            data=json.dumps(update_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 500)


if __name__ == "__main__":
    unittest.main()
