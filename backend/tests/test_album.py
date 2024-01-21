import unittest
import json
import sys
import datetime
sys.path.append("..")
from app import create_app

test_album_id = None
test_album_data = {
            "Name": "Test Album15",
            "Image": "https://example.com/image.jpg",
            "Release Date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "Total Tracks": 10,
            "Songs": ["Song 1", "Song 2"],
            "Artists": ["Artist 1", "Artist 2"]
        }
class AlbumBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test10_create_album(self):
        response = self.client.post(
            "/album/create",
            data=json.dumps(test_album_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode())
        self.assertIn("New album created!", data["message"])
        global test_album_id
        test_album_id = data.get("album_id")

    def test12_get_album(self):
        response = self.client.get(f"/album/{test_album_id}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn("album", data)

    def test13_get_album_by_name(self):
        response = self.client.get(f"/album/get_by_name/{test_album_data['Name']}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn("album", data)

    def test14_update_album(self):
        update_data = {"Name": "Updated Album Name"}
        response = self.client.put(
            f"/album/{test_album_id}",
            data=json.dumps(update_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn("Album updated!", data["message"])
        
    def test15_delete_album(self):
        response = self.client.delete(f"/album/{test_album_id}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn("Album deleted!", data["message"])

    def test16_get_all_albums(self):
        response = self.client.get("/album/all")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn("album_ids", data)

    ### Error Handling Tests ###

    def test17_create_album_missing_fields(self):
        incomplete_data = {"Name": "Incomplete Album"}
        response = self.client.post(
            "/album/create",
            data=json.dumps(incomplete_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test18_get_nonexistent_album(self):
        response = self.client.get("/album/nonexistent_album_id")
        self.assertEqual(response.status_code, 500)

    def test19_update_nonexistent_album(self):
        response = self.client.put(
            "/album/nonexistent_album_id",
            data=json.dumps({"Name": "Doesn't exist"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 500)


if __name__ == "__main__":
    unittest.main()
