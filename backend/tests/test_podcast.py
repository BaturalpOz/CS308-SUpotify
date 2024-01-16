import sys
import unittest
import json
import random
sys.path.append("..")
from app import create_app

test_podcast_id = None
name_podcast = "TestPodcast" + str(random.randint(0, 1000))
class PodcastBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
    def test1_get_podcasts(self):
        response = self.client.get('/podcast/get-podcasts')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test2_create_podcast(self):
        response = self.client.post('/podcast/add-podcast', data=json.dumps(dict(name=name_podcast)), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        global test_podcast_id
        test_podcast_id = json.loads(response.data)

    def test4_add_episode(self):
        response = self.client.post('/podcast/add-episode', data=json.dumps(dict(episode_name="TestEpisode1", podcast_name=name_podcast, duration="1500", description="testdesc")), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test5_get_podcast(self):
        response = self.client.post('/podcast/get-podcast', data=json.dumps(dict(podcast_name=name_podcast)), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test6_delete_podcast(self):
        response = self.client.post('/podcast/delete-podcast', data=json.dumps(dict(id=test_podcast_id)), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        


if __name__ == "__main__":
    unittest.main()