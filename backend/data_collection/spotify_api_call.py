import requests
import base64
from dotenv import load_dotenv
import json
import os
import pandas as pd

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")


def get_access_token(client_id, client_secret):
    token_url = "https://accounts.spotify.com/api/token"

    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode())

    token_data = {"grant_type": "client_credentials"}
    token_headers = {"Authorization": f"Basic {client_creds_b64.decode()}"}
    response = requests.post(token_url, data=token_data, headers=token_headers)
    token_response_data = response.json()
    access_token = token_response_data.get("access_token")

    return access_token


def get_top_artists(access_token, limit=25):
    top_artists_url = "https://api.spotify.com/v1/browse/new-releases"

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(top_artists_url, headers=headers, params={"limit": limit})
    artists = response.json()["albums"]["items"]

    artist_data = {}
    for artist in artists:
        artist_id = artist["artists"][0]["id"]
        artist_data[artist_id] = {"Name": artist["artists"][0]["name"], "Albums": []}

    return artist_data


def get_albums_for_artist(access_token, artist_id):
    albums_url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(albums_url, headers=headers)
    albums = response.json()["items"]

    albums = albums[:3] if len(albums) > 3 else albums

    album_data = {}
    for album in albums:
        artists = []
        for artist in album["artists"]:
            artists.append(artist["name"])
        album_id = album["id"]
        album_data[album_id] = {
            "Name": album["name"],
            "Image": album["images"][0]["url"],
            "Release Date": album["release_date"],
            "Total Tracks": album["total_tracks"],
            "Songs": [],
            "Artists": artists,
        }

    return album_data


def get_songs_for_album(access_token, album_id):
    tracks_url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(tracks_url, headers=headers)
    songs = response.json()["items"]

    song_data = {}
    for i, song in enumerate(songs):
        song_data[i] = {}
        song_data[i]["id"] = song["id"]
        song_data[i]["Name"] = song["name"]
        song_data[i]["Duration_ms"] = song["duration_ms"]

    return song_data


def get_audio_features_for_song(access_token, song_id):
    audio_features_url = f"https://api.spotify.com/v1/audio-features/{song_id}"

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(audio_features_url, headers=headers)
    audio_features = response.json()

    return audio_features


def get_artist_info(access_token, artist_id):
    artist_url = f"https://api.spotify.com/v1/artists/{artist_id}"

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(artist_url, headers=headers)
    artist_info = response.json()

    return artist_info


access_token = get_access_token(client_id, client_secret)

artist_data = get_top_artists(access_token)

for artist_id in artist_data.keys():
    artist_info = get_artist_info(access_token, artist_id)
    artist_data[artist_id]["Genres"] = artist_info["genres"]
    artist_data[artist_id]["Popularity"] = artist_info["popularity"]
    artist_data[artist_id]["Image"] = artist_info["images"][0]["url"]

    album_data = get_albums_for_artist(access_token, artist_id)
    for album_id in album_data.keys():
        song_data = get_songs_for_album(access_token, album_id)

        for i, song in enumerate(song_data.values()):
            song_id = song["id"]
            audio_features = get_audio_features_for_song(access_token, song_id)
            song["Danceability"] = (
                audio_features["danceability"] if audio_features["danceability"] else 0
            )
            song["Energy"] = audio_features["energy"] if audio_features["energy"] else 0
            song["Loudness"] = (
                audio_features["loudness"] if audio_features["loudness"] else 0
            )
            song["Tempo"] = audio_features["tempo"] if audio_features["tempo"] else 0

            song_data[i] = song
        album_data[album_id]["Songs"].append(song_data)

    artist_data[artist_id]["Albums"].append(album_data)

with open("data/spotify_data.json", "w") as outfile:
    json.dump(artist_data, outfile, indent=4)

# GET PODCASTS

podcasts = pd.DataFrame()
id_list = []
name_list = []
desc_list = []


def get_podcasts(search):
    endpoint_url = "https://api.spotify.com/v1/search?q=music&type=show&market=US"

    limit = 50  
    offset = 0  

    more_runs = 5 
    counter = 0
    while (offset <= 1950) & (
        counter <= more_runs
    ):  
        query = f"{endpoint_url}&offset={offset}&limit={limit}"  

        response = requests.get(
            query,  # get request
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        )
        json_response = response.json()  # as a json file
        try:
            for i in range(len(json_response["shows"]["items"])):  # loop through json
                id_list.append(
                    json_response["shows"]["items"][i]["id"]
                )  # pull out info from json
                name_list.append(
                    json_response["shows"]["items"][i]["name"]
                )  # into empty lists
                desc_list.append(json_response["shows"]["items"][i]["description"])
        except:
            break

        counter += 1  # increase conditional counter by 1

        offset = offset + 50


all_data = []
get_podcasts("music")

podcasts["id"] = id_list
podcasts["name"] = name_list
podcasts["description"] = desc_list


def get_episodes(id, name):
    endpoint_url = f"https://api.spotify.com/v1/shows/{id}/episodes"
    episode_data = []

    response = requests.get(
        endpoint_url,  # get request
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )
    json_response = response.json()
    data = {"podcast_id": id, "podcast_name": name, "episodes": []}

    for i in range(len(json_response["items"])):
        data["episodes"].append(
            {
                "episode_name": json_response["items"][i]["name"],
                "episode_duration": json_response["items"][i]["duration_ms"],
                "episode_id": json_response["items"][i]["id"],
                "episode_description": json_response["items"][i]["description"],
            }
        )

    all_data.append(data)

for i, row in podcasts.iterrows():
  try:
    get_episodes(row["id"], row["name"])
  except Exception as e:
    print(e)
    continue

json.dump(all_data, open("./podcasts.json",'w+'),indent=2)