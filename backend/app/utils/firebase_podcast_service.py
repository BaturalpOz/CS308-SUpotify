import firebase_admin
from firebase_admin import credentials, firestore
from app.models.Podcast import Podcast, Episode
import os
from typing import Dict

class FirebasePodcastService:
    def __init__(self):
        if not firebase_admin._apps:
            cred_path = os.getenv('FIREBASE_ADMINSDK_JSON_PATH')
            if cred_path is None:
                raise ValueError("The FIREBASE_ADMINSDK_JSON_PATH environment variable must be set.")
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)

        self.db = firestore.client()

    def add_podcast(self, podcast: Podcast):
        """
        Adds a new podcast document to the Podcasts collection.
        """
     
        podcast_dict = podcast.to_dict()
        try:
            _, doc_ref = self.db.collection(u'Podcasts').add(podcast_dict)
            return doc_ref.id  
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def add_episode(self, podcast_name: str, episode: Episode):
        """
        Adds a new episode document to the Episodes collection.
        """
        episode_dict = episode.to_dict()
        podcast_id = self.get_podcast_by_name(podcast_name)
        print(podcast_id)
        try:
            episodes_ref = self.db.collection(u'Podcasts').document(podcast_id).collection(u'Episodes')
            _, doc_ref = episodes_ref.add(episode_dict)
            return doc_ref.id
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    def get_podcast(self, podcast_id: str) -> Dict:
        """
        Returns a dictionary representing a podcast document.
        """
        try:
            doc_ref = self.db.collection(u'Podcasts').document(podcast_id)
            doc = doc_ref.get()
            if not doc.exists:
                return None
            return doc.to_dict()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    def get_podcast_by_name(self, podcast_name: str) -> Dict:
        """
        Returns a dictionary representing a podcast document.
        """
        try:
            docs = self.db.collection(u'Podcasts').where(u'name', u'==', podcast_name).stream()
            return {doc.id: doc.to_dict() for doc in docs}
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    def get_episode_by_name(self, podcast_name: str, episode_name: str) -> Dict:
        """
        Returns a dictionary representing an episode document.
        """
        try:
            podcast_id = self.get_podcast_by_name(podcast_name)
            docs = self.db.collection(u'Podcasts').document(podcast_id).collection(u'Episodes').where(u'name', u'==', episode_name).stream()
            return {doc.id: doc.to_dict() for doc in docs}
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def update_podcast(self, podcast_id: str, podcast: Podcast) -> bool:
        """
        Updates an existing podcast document.
        """
        try:
            doc_ref = self.db.collection(u'Podcasts').document(podcast_id)
            doc_ref.update(podcast.to_dict())
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def update_episode(self, podcast_id: str, episode_id: str, episode: Episode) -> bool:
        """
        Updates an existing episode document.
        """
        try:
            doc_ref = self.db.collection(u'Podcasts').document(podcast_id).collection(u'Episodes').document(episode_id)
            doc_ref.update(episode.to_dict())
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def delete_podcast(self, podcast_id: str) -> bool:
        """
        Deletes a podcast document.
        """
        try:
            doc_ref = self.db.collection(u'Podcasts').document(podcast_id)
            doc_ref.delete()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        
    def delete_episode(self, podcast_id: str, episode_id: str) -> bool:
        """
        Deletes an episode document.
        """
        try:
            doc_ref = self.db.collection(u'Podcasts').document(podcast_id).collection(u'Episodes').document(episode_id)
            doc_ref.delete()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        
    def get_podcasts(self) -> Dict:
        """
        Returns a dictionary representing all podcast documents.
        """
        try:
            docs = self.db.collection(u'Podcasts').stream()
            return {doc.id: doc.to_dict() for doc in docs}
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_episodes(self, podcast_id: str) -> Dict:
        """
        Returns a dictionary representing all episode documents for a podcast.
        """
        try:
            docs = self.db.collection(u'Podcasts').document(podcast_id).collection(u'Episodes').stream()
            return {doc.id: doc.to_dict() for doc in docs}
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    def get_podcast_episodes(self, podcast_id: str) -> Dict:
        """
        Returns a dictionary representing all episode documents for a podcast.
        """
        try:
            docs = self.db.collection(u'Podcasts').document(podcast_id).collection(u'Episodes').stream()
            return {doc.id: doc.to_dict() for doc in docs}
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    

