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
        podcast_id = self.get_podcast_by_name(podcast_name)['id']
        try:
            podcast_ref = self.db.collection(u'Podcasts').document(podcast_id)
            podcast_ref.update({u'Episodes': firestore.ArrayUnion([episode_dict])})
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
            doc = doc.to_dict()
            return doc
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    def get_podcast_by_name(self, podcast_name: str) -> Dict:
        """
        Returns a dictionary representing a podcast document.
        """
        try:
            docs = self.db.collection(u'Podcasts').where(u'Name', u'==', podcast_name).stream()
            result = None
            for doc in docs:
                id_doc = doc.id
                doc = doc.to_dict()
                result = doc
                result['id'] = id_doc
            if result is None:
                return None
            
            return result
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    def get_episode_by_name(self, podcast_name: str, episode_name: str) -> Dict:
        """
        Returns a dictionary representing an episode document.
        """
        try:
            podcast_id = self.get_podcast_by_name(podcast_name)['id']
            docs = self.db.collection(u'Podcasts').document(podcast_id)
            # get episode from episode array in podcast document
            for episode in docs.get().to_dict()['Episodes']:
                if episode['Name'] == episode_name:
                    return episode
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
        
        
    def get_podcasts(self) -> Dict:
        """
        Returns a dictionary representing all podcast documents.
        """
        try:
            docs = self.db.collection(u'Podcasts').stream()
            return {doc.id: doc.to_dict() for doc in docs}
        except Exception as e:
            print(f"An error occurred All: {e}")
            return None

    def get_episodes(self, podcast_id: str) -> Dict:
        """
        Returns a dictionary representing all episode documents for a podcast.
        """
        try:
            docs = self.db.collection(u'Podcasts').document(podcast_id)
            return docs.get().to_dict()['Episodes']
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    def get_podcast_episodes(self, podcast_id: str) -> Dict:
        """
        Returns a dictionary representing all episode documents for a podcast.
        """
        try:
            docs = self.db.collection(u'Podcasts').document(podcast_id)
            return docs.get().to_dict()['Episodes']
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    

