import unittest
import json
import sys
import random
sys.path.append("..")
from app import create_app

test_artist_name = f"Test Artist {random.randint(0, 10000)}"
test_artist_id = None
class ArtistBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()


    def test10_create_artist(self):
        artist_data = {
            "Name": test_artist_name,
            "Genres": ["Pop", "Rock"],
            "Image": "test_image_url",
            "Popularity": 80,
            "Albums": ["Test Album 1"]
        }
        response = self.client.post(
            "/artist/create",
            data=json.dumps(artist_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode())
        self.assertIn("New artist created!", data["message"])
        global test_artist_id
        test_artist_id = data.get("artist_id")

    def test11_get_artist(self):
        if not test_artist_id:
            self.fail("No artist ID available for test.")
        response = self.client.get(f"/artist/{test_artist_id}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn("artist", data)

    def test13_update_artist(self):
        if not test_artist_id:
            self.fail("No artist ID available for test.")
        update_data = {"Popularity": 90}
        response = self.client.put(
            f"/artist/{test_artist_id}",
            data=json.dumps(update_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn("Artist updated!", data["message"])

    def test14_get_all_artists(self):
        response = self.client.get("/artist/all")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn("artists", data)

    def test15_get_artist_by_name(self):
        response = self.client.get(f"/artist/get_by_name/{test_artist_name}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn("artist", data)

    def test16_delete_artist(self):
        if not test_artist_id:
            self.fail("No artist ID available for test.")
        response = self.client.delete(f"/artist/{test_artist_id}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn("Artist deleted!", data["message"])

    ### Error Handling Tests ###

    def test17_create_artist_missing_fields(self):
        response = self.client.post(
            "/artist/create",
            data=json.dumps({"Name": "Incomplete Artist"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test18_get_nonexistent_artist(self):
        response = self.client.get("/artist/nonexistent_artist_id")
        self.assertEqual(response.status_code, 500)

    def test19_update_nonexistent_artist(self):
        response = self.client.put(
            "/artist/nonexistent_artist_id",
            data=json.dumps({"Popularity": 90}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 500)


if __name__ == "__main__":
    unittest.main()
