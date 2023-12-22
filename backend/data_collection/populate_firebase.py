import sys 

sys.path.append("..")
from app import create_app

import json 

spotify_data = json.load(open("data/spotify_data.json", "r"))

app = create_app()

def get_song_names_in_album(songs):
    song_names = []
    for song in songs.values():
        song_names.append(song["Name"])
    return song_names

def create_albums(artist_data):
    for album in artist_data["Albums"][0].values():
        album_name = album["Name"]
        image_url = album["Image"]
        release_date = album["Release Date"]
        total_tracks = album["Total Tracks"]
        songs = get_song_names_in_album(album["Songs"][0])
        artists = album["Artists"]
        response = app.test_client().post(
            "/album/create",
            data=json.dumps({
                "Name": album_name,
                "Image": image_url,
                "Release Date": release_date,
                "Total Tracks": total_tracks,
                "Songs": songs,
                "Artists": artists
            }),
            content_type="application/json"
        )

def create_artists(artist_data):
    artist_name = artist_data["Name"]
    genres = artist_data["Genres"]
    image_url = artist_data["Image"]
    popularity = artist_data["Popularity"]
    albums = []
    for album in artist_data["Albums"][0].values():
        albums.append(album["Name"])
    response = app.test_client().post(
        "/artist/create",
        data=json.dumps({
            "Name": artist_name,
            "Genres": genres,
            "Image": image_url,
            "Popularity": popularity,
            "Albums": albums
        }),
        content_type="application/json"
    )

def create_songs(artist_data):
    for album in artist_data["Albums"][0].values():
        for song in album["Songs"][0].values():
            song_name = song["Name"]
            duration_ms = song["Duration_ms"]
            danceability = song["Danceability"]
            energy = song["Energy"]
            loudness = song["Loudness"]
            tempo = song["Tempo"]
            albums = [album["Name"]]
            artists = album["Artists"]
            response = app.test_client().post(
                "/song/songs",
                data=json.dumps({
                    "Name": song_name,
                    "Duration": duration_ms,
                    "Danceability": danceability,
                    "Energy": energy,
                    "Loudness": loudness,
                    "Tempo": tempo,
                    "Albums": albums,
                    "Artists": artists
                }),
                content_type="application/json"
            )
            print(response.data)

def create_everything(spotify_data):
    for artist_id in spotify_data:
        artist_data = spotify_data[artist_id]
        create_albums(artist_data)
        create_artists(artist_data)
        create_songs(artist_data)

create_everything(spotify_data)
