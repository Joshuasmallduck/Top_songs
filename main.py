import requests
import base64
import json

client_id = #Your client id
client_secret = #Your secret key

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=data)
    json_result = response.json()
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = {"q": artist_name, "type": "artist", "limit": 1}

    response = requests.get(url, headers=headers, params=query)
    json_result = response.json()
    if len(json_result["artists"]["items"]) == 0:
        print("No artist with this name exists...")
        return None

    return json_result["artists"]["items"][0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    response = requests.get(url, headers=headers)
    json_result = response.json()
    return json_result["tracks"]

name = input("What is your artists name?")
token = get_token()
artist = search_for_artist(token, name)
if artist is not None:
    songs = get_songs_by_artist(token, artist["id"])
    for idx, song in enumerate(songs):
        print(f"{idx+1}. {song['name']}")
