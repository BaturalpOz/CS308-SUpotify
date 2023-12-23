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

    def generate_recommendations(self, user_id: str) -> Dict[str, List[Song]]:
        """
        Generate music recommendations for a user.
        """
        user = self.firebase_user_service.get_user(user_id)
        recommendations = {
            "from_ratings": self._recommend_from_ratings(user.rated_songs),
            "from_friends": self._recommend_from_friends(user.friends),
            # "from_subscriptions": self._recommend_from_subscriptions(user)
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
                    if song in user.rated_songs:
                        recommendations[key].remove(song)

        # Randomly select 10 songs from each recommendation category
        for key in recommendations:
            random.shuffle(recommendations[key])
            recommendations[key] = (
                recommendations[key][:10]
                if len(recommendations[key]) > 10
                else recommendations[key]
            )

        return recommendations

    def _recommend_from_ratings(self, rated_songs: List[dict]) -> List[Song]:
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

                song = self.firebase_artist_service.get_song_by_name(entry["song"])
                danceability, energy, loudness, tempo = (
                    song.danceability,
                    song.energy,
                    song.loudness,
                    song.tempo,
                )

                similar_songs = self._find_similar_songs(
                    genres, danceability, energy, loudness, tempo
                )
                recommended_songs.extend(similar_songs)

        recommended_songs = list(set(recommended_songs))
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
            recommended_songs.append(friend_recs)
        recommended_songs = list(set(recommended_songs))
        return recommended_songs

    def _recommend_from_subscriptions(self,user:User) -> List[Song]:
        """
        Recommend songs based on subscribed artists' activities.
        """
        subscriptions = user.subscribed_artists
        recommended_songs = []
        
        user_rated_songs = user.rated_songs
        
        for artist_id in subscriptions:
            
            artist_songs = self.artist_service.get_artist_songs(artist_id)
            artist = self.artist_service.get_artist_by_id(artist_id)

            # Recommend songs from subscribed artist that user hasn't rated yet
            
            for song in artist_songs:
                if song.name not in user_rated_songs:
                    recommended_songs.append(song)
            # Recommend songs similar to subscribed artists
                danceability, energy, loudness, tempo = (
                    song.danceability,
                    song.energy,
                    song.loudness,
                    song.tempo,
                    )
                genres = artist.genres
                similar_songs = self._find_similar_songs(
                genres, danceability, energy, loudness, tempo
                )
                recommended_songs.extend(similar_songs)
            
       

        recommended_songs = list(set(recommended_songs))
        return recommended_songs

    def _get_new_songs_by_artist(
        self, artist_name: str, subscription_date: datetime
    ) -> List[Song]:
        """
        Get new songs added by the subscribed artist since the subscription date.
        """
        new_songs = []
        subscribed_artist = self.artist_service.get_artist_by_name(artist_name)

        for song in subscribed_artist.songs:
            # Replace 'release_date' with the actual attribute in your Song class
            if song.release_date > subscription_date:
                new_songs.append(song)

        return new_songs

    def _find_similar_songs(
        self,
        genres: List[str],
        danceability: float,
        energy: float,
        loudness: float,
        tempo: float,
    ) -> List[Song]:
        """
        Find songs that are similar to the provided song characteristics.
        """
        all_songs = self.song_service.get_all_songs()

        similar_songs = []
        for song in all_songs:
            artists = song.artists
            song_genres = []
            for artist in artists:
                artist_obj = self.artist_service.get_artist_by_name(artist)
                song_genres.extend(artist_obj.genres)

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
        danceability_diff = abs(song.danceability - target_danceability)
        energy_diff = abs(song.energy - target_energy)
        loudness_diff = abs(song.loudness - target_loudness)
        tempo_diff = abs(song.tempo - target_tempo)

        danceability_score = 1 - danceability_diff if danceability_diff < 0.1 else 0
        energy_score = 1 - energy_diff if energy_diff < 0.1 else 0
        loudness_score = 1 - loudness_diff / 10 if loudness_diff < 10 else 0
        tempo_score = 1 - tempo_diff / 10 if tempo_diff < 10 else 0

        combined_score = (
            danceability_score + energy_score + loudness_score + tempo_score
        ) / 4

        return combined_score
    
