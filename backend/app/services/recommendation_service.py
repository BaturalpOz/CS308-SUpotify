import random
from datetime import datetime, timedelta
from typing import List, Dict
from app.models.Song import Song
from app.utils.firebase_artist_service import FirebaseArtistService
from app.utils.firebase_song_service import FirebaseSongService
from app.utils.firebase_user_service import FirebaseUserService
from app.services.user_service import UserService
from app.services.artist_service import ArtistService
from app.models.User import User
from app.services.song_service import SongService


class RecommendationService:
    def __init__(self):
        self.user_service = UserService()
        self.artist_service = ArtistService()
        self.song_service = SongService()
        self.firebase_user_service = FirebaseUserService()
        self.firebase_song_service = FirebaseSongService()
        self.firebase_artist_service = FirebaseArtistService()
        self.all_songs = self.song_service.get_all_songs_with_ids()  # Only accessing the database once for efficency purposes.
        self.all_artists = self.artist_service.get_all_artists()  # This is necessary because there are some songs in the DB
                                                                 # that the corresponding artist isnt in the DB.

    def generate_recommendations(self, user_id: str):
        """
        Generate music recommendations for a user.
        """
        user = self.firebase_user_service.get_user(user_id)
        recommendations = {
           "from_ratings": self._recommend_from_ratings(user.rated_songs),
           "from_friends": self._recommend_from_friends(user.friends),
           "from_subscriptions": self._recommend_from_subscriptions(user)
        }

        # Delete songs that are recomended and are in user.rated_songs
        for key in recommendations:
            if "from_friends" in key:
                for friend in recommendations[key]:
                    for song in friend["songs"]:
                        if song in user.rated_songs:
                            friend["songs"].remove(song)
            else:
                for song in recommendations[key]:
                    if song["Id"] in user.rated_songs:
                        recommendations[key].remove(song)

        # Randomly select 10 songs from each recommendation category
        for key in recommendations:
            random.shuffle(recommendations[key])
            recommendations[key] = (
                recommendations[key][:10]
                if len(recommendations[key]) > 10
                else recommendations[key]
            )
        recommendations = [recommended_song["Name"] for recommended_song in recommendations["from_subscriptions"]]
        return recommendations

    def _recommend_from_ratings(self, rated_songs: List[dict]):
        """
        Recommend songs based on user's rated songs.
        """
        recommended_songs = []
        for entry in rated_songs:
            if entry["rating"] > 3 and entry["date"] > datetime.now() - timedelta(
                days=3
            ):
                artists = entry["artists"]
                genres = []
                for artist in artists:
                    artist_obj = self.artist_service.get_artist_by_name(artist)
                    genres.extend(artist_obj.genres)

                song = self.find_in_list_by_name(entry["song"])
                danceability, energy, loudness, tempo = (
                    song["Danceability"],
                    song["Energy"],
                    song["Loudness"],
                    song["Tempo"]
                )

                similar_songs = self._find_similar_songs(
                    genres, danceability, energy, loudness, tempo
                )
                if similar_songs:
                    for song in similar_songs:
                         if song not in recommended_songs:
                             recommended_songs.append(song)
        return recommended_songs

    def _recommend_from_friends(self, friends: List[dict]) -> List[Song]:
        """
        Recommend songs based on friends' activities.
        """
        recommended_songs = []
        for friend in friends:
            includeInRecommendations = friend["User_Settings"][
                "includeInRecommendations"
            ]
            friend_name = friend["friendUsername"]
            friend_user = self.firebase_user_service.get_user_by_username(friend_name)
            friend_rated_songs = friend_user.rated_songs
            friend_recs = {
                "username": friend_name if includeInRecommendations else "",
                "songs": self._recommend_from_ratings(friend_rated_songs)
            }
             
            for song in friend_recs["songs"]:
                if song not in recommended_songs:
                    recommended_songs.append(song)
        return recommended_songs

    def _recommend_from_subscriptions(self,user:User):
        """
        Recommend songs based on subscribed artist's activities.
        """
        subscriptions = user.subscribed_artists
        recommended_songs = []
        user_rated_songs = user.rated_songs
        
        for artist_id in subscriptions:
            artist = self.find_in_list(artist_id,self.all_artists)
            artist_songs = self.find_artist_songs(artist["Name"]) # This method returns a list of indexes                                                                                
            danceability_sum = 0                                  # since working with indexes avoids redundant memory usage. 
            energy_sum = 0
            loudness_sum = 0
            tempo_sum = 0
            counter = 0
            for song_index in artist_songs:  # Recommend songs from subscribed artist that user hasn't rated yet
                song = self.all_songs[song_index]
                if song["Name"] not in user_rated_songs:
                    recommended_songs.append(song)
                danceability_sum += song["Danceability"]
                energy_sum += song["Energy"]
                loudness_sum += song["Loudness"]
                tempo_sum += song["Tempo"]
                counter += 1
            # Take the average of each song of the artist, recommend based on that
            # This is efficent assuming an artist's songs are similar to eachother
            # Thus, eliminating reduntant calculation that stems from repeatedly calculating the same songs
            if counter > 0:
                danceability = danceability_sum/counter
                energy = energy_sum/counter
                loudness = loudness_sum/counter
                tempo = tempo_sum/counter

            genres = artist["Genres"]
            # Recommend songs similar to subscribed artists
            similar_songs = self._find_similar_songs(
            genres, danceability, energy, loudness, tempo
            )
            if similar_songs:
                for song in similar_songs:
                    if song not in recommended_songs:
                        recommended_songs.append(song)
        return recommended_songs

    def artists_in_song_list(self,song_list:List[Song]):
        '''returns the lists of artists in a set of songs'''
        artist_list = []
        for song in song_list:
            artist_list.append(song.artists)
        return artist_list

    def find_artist_songs(self,artist_name:str):
        '''returns the indexes of the songs that belong to the artist'''
        artist_songs = []
        index_counter = 0
        for song in self.all_songs:
            if artist_name in song["Artists"]:
                artist_songs.append(index_counter)
            index_counter += 1
        return artist_songs
    
    def find_in_list(self,item_id:str,list):
        for item in list:
            if item_id==item["Id"]:
                return item
        return None
    def find_in_list_by_name(self,item_name:str,list):
        for item in list:
            if item_name==item["Name"]:
                return item
        return None

    def _remove_shared_songs(self,list1, list2):
        #Removes songs from list1 that occurs in both list1 and list2
        return_list = [song for song in list1 if song not in list2]
        return return_list

    def _find_similar_songs(
        self,
        genres: List[str],
        danceability: float,
        energy: float,
        loudness: float,
        tempo: float,
    ):
        artist_names = [artist["Name"] for artist in self.all_artists]
        '''Finds similar songs in a given set of songs'''
        similar_songs = []
        for song in self.all_songs:
            
            artists = song["Artists"]
            song_genres = []
            # for artist in artists: 
            artist_name = artists[0]
            if artist_name in artist_names:          
                artist = self.find_in_list(artist_name,self.all_artists)
                if artist:
                    song_genres.extend(artist["Genres"])

            similarity_score = self._compute_similarity_score(
                song, danceability, energy, loudness, tempo
            )
            if self._is_genre_match(song_genres, genres) and similarity_score > 0.60:
                similar_songs.append(song)

        return similar_songs
    
    def _is_genre_match(self, song_genres: List[str], target_genres: List[str]) -> bool:
        """
        Check if the song's genres match any of the target genres.
        """
        return any(genre in target_genres for genre in song_genres)

    def _compute_similarity_score(
        self,
        song: Song,
        target_danceability: float,
        target_energy: float,
        target_loudness: float,
        target_tempo: float,
    ) -> float:
        """
        Compute a similarity score for a song based on a simple attribute distance formula.
        """
        danceability_diff = abs(song["Danceability"] - target_danceability)
        energy_diff = abs(song["Energy"] - target_energy)
        loudness_diff = abs(song["Loudness"] - target_loudness)
        tempo_diff = abs(song["Tempo"] - target_tempo)

        danceability_score = 1 - danceability_diff if danceability_diff < 0.1 else 0
        energy_score = 1 - energy_diff if energy_diff < 0.1 else 0
        loudness_score = 1 - loudness_diff / 10 if loudness_diff < 10 else 0
        tempo_score = 1 - tempo_diff / 10 if tempo_diff < 10 else 0

        combined_score = (
            danceability_score + energy_score + loudness_score + tempo_score
        ) / 4

        return combined_score
    
