import sys
import unittest
import json

sys.path.append("..")
from app import create_app

test_album_id = None

class AlbumBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        self.test_album_data = {
            "Name": "Test Album",
            "Image": "https://example.com/image.jpg",
            "Languages": "English",
            "Release Country": "United States",
            "Release Date": "2023-11-19T14:32:04", # Date format should be exactly like this, this is subject to change
            "Songs": ["Song 1", "Song 2"],
            "Title": "Test Title"
        }

    def test1_create_album(self):
        global test_album_id
        response = self.client.post(
            "/album/create",
            data=json.dumps(self.test_album_data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode())
        self.assertIn("New album created!", data["message"])
        self.assertTrue("album_id" in data)

        test_album_id = data["album_id"]
    
   

    def test2_get_album(self):
        if not test_album_id:
            self.fail("No artist ID available for test.")
        response = self.client.get(f"/album/{test_album_id}")  # Assuming you know the album ID from the previous test
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertTrue("album" in data)

    def test3_update_album(self):
        if not test_album_id:
            self.fail("No artist ID available for test.")
        response = self.client.put(
            f"/album/{test_album_id}",  # Assuming you know the album ID from the previous test
            data=json.dumps({"name": "Updated Album"}),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn("Album updated!", data["message"])

    def test4_delete_album(self):
        if not test_album_id:
            self.fail("No artist ID available for test.")
        response = self.client.delete(f"/album/{test_album_id}")  # Assuming you know the album ID from the previous test
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn("Album deleted!", data["message"])

    def test5_get_all_albums(self):
        if not test_album_id:
            self.fail("No artist ID available for test.")
        response = self.client.get("/album/all")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertTrue("album_ids" in data)

if __name__ == "__main__":
    unittest.main()
