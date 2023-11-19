import unittest
import json
import sys

sys.path.append("..")
from app import create_app

test_token = None
test_artist_id = None

class ArtistBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        self.test_artist_data = {
            "Name": "Test Artist",
            "Description": "Test Description",
            "Image": "test_image_url",
            "Albums" : []
        }

    def test1_create_artist(self):
        global test_artist_id

        response = self.client.post(
            "/artist/create",
            data=json.dumps(self.test_artist_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode())
        self.assertIn("New artist created!", data["message"])
        self.assertTrue("artist_id" in data)

        test_artist_id = data["artist_id"]

    def test2_get_artist(self):
        if not test_artist_id:
            self.fail("No artist ID available for test.")

        response = self.client.get(
            f"/artist/{test_artist_id}",
            headers={"x-access-token": test_token},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertTrue("artist" in data)

    def test3_update_artist(self):
        if not test_artist_id:
            self.fail("No artist ID available for test.")

        response = self.client.put(
            f"/artist/{test_artist_id}",
            headers={"x-access-token": test_token},
            data=json.dumps({"Description": "Updated Description"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn("Artist updated!", data["message"])

    
    def test4_get_all_artists(self):
        response = self.client.get(
            "/artist/all",
            headers={"x-access-token": test_token},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertTrue("artist_ids" in data)
    def test5_get_artist_by_name(self):
        response = self.client.get('/artist/get_by_name/Test Artist')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertTrue("artist" in data)
        self.assertEqual(data["artist"]["Name"], "Test Artist")
    def test6_delete_artist(self):
        if not test_artist_id:
            self.fail("No artist ID available for test.")

        response = self.client.delete(
            f"/artist/{test_artist_id}",
            headers={"x-access-token": test_token},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn("Artist deleted!", data["message"])

if __name__ == "__main__":
    unittest.main()
