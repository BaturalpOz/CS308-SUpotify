from app.utils.firebase_podcast_service import FirebasePodcastService
from app.models.Podcast import Podcast, Episode
from typing import List


class PodcastService:
    def __init__(self):
        self.firebase_podcast_service = FirebasePodcastService()

    def create_podcast(self, name: str, episodes: List[Episode]) -> str:
        """
        Handles the business logic for creating a new album.
        """
        if self.firebase_podcast_service.get_podcast_by_name(name):
            raise ValueError("A podcast with that name already exists.")

        # Create a new Album instance
        new_podcast = Podcast(name=name, episodes=episodes)

        # Add the new album to Firebase, which returns the album_id if successful
        podcast_id = self.firebase_podcast_service.create_podcast(new_podcast)

        if podcast_id:
            return podcast_id
        else:
            raise Exception("Failed to create a new podcast in Firebase.")
    
    def get_podcast(self, podcast_name: str) -> Podcast:
        return self.firebase_podcast_service.get_podcast_by_name(podcast_name)

    def get_podcasts(self) -> List[Podcast]:
        return self.firebase_podcast_service.get_podcasts()

    def update_podcast(self, podcast: Podcast) -> Podcast:
        return self.firebase_podcast_service.update_podcast(podcast)
    
    def delete_podcast(self, podcast_id: str) -> None:
        return self.firebase_podcast_service.delete_podcast(podcast_id)
    
    def create_episode(self, podcast_name: str, episode_name: str, episode_duration: int) -> Episode:
        episode = Episode(name=episode_name, duration=episode_duration)
        episode_id = self.firebase_podcast_service.create_episode(podcast_name, episode)
        if episode_id:
            return episode
        else:
            raise Exception("Failed to create a new episode in Firebase.")

    def get_episode(self, podcast_id: str, episode_id: str) -> Episode:
        return self.firebase_podcast_service.get_episode(podcast_id, episode_id)
    
    def get_episodes(self, podcast_id: str) -> List[Episode]:
        return self.firebase_podcast_service.get_episodes(podcast_id)
    
