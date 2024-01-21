import sys
import unittest
import json
import random
sys.path.append("..")
from app import create_app

test_podcast_name = "TestPodcast" + str(random.randint(0, 1000))
test_podcast_id = None
class PodcastBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test10_create_podcast(self):
        response = self.client.post(
            '/podcast/add-podcast',
            data=json.dumps({"name": test_podcast_name}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        global test_podcast_id
        test_podcast_id = data

    def test12_get_podcasts(self):
        response = self.client.get('/podcast/get-podcasts')
        self.assertEqual(response.status_code, 200)

    def test13_add_episode(self):
        episode_data = {
            "episode_name": "TestEpisode",
            "duration": 1500,
            "podcast_name": test_podcast_name,
            "description": "Test Description"
        }
        response = self.client.post(
            '/podcast/add-episode',
            data=json.dumps(episode_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn("Name", data)
        self.assertIn("Duration", data)
        self.assertIn("Description", data)

    def test14_get_podcast_by_name(self):
        response = self.client.get(f'/podcast/get-podcast?podcast_name={test_podcast_name}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertIn("Name", data)

    def test15_delete_podcast(self):
        response = self.client.post(
            '/podcast/delete-podcast',
            data=json.dumps({"id": test_podcast_id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    ### Error Handling Tests ###

    def test16_create_podcast_missing_name(self):
        response = self.client.post(
            '/podcast/add-podcast',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test17_add_episode_missing_fields(self):
        episode_data = {
            # Missing required fields
        }
        response = self.client.post(
            '/podcast/add-episode',
            data=json.dumps(episode_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test18_get_nonexistent_podcast(self):
        response = self.client.get('/podcast/get-podcast?podcast_name=NonExistentPodcast')
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()