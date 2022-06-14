import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "6790641968674996816548c9a2a8d469"
CLIENT_SECRET = "7accf1f53de741f589387c489228a70b"
redirect_url = "https://example.com"

date = input("Which year do you want to travel to?Type the date in the format YYYY-MM-DD:")

response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}/")
contents = response.text

soup = BeautifulSoup(contents, "html.parser")

songs = [a.getText().strip() for a in soup.select("li #title-of-a-story")]
print(songs)
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=redirect_url,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
song_uris = []
year = date.split("-")[0]

for song in songs:
    get_song = sp.search(f"track:{song} year:{year}")
    try:
        uri = get_song["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} does not exist.")

print(song_uris)
playlist = sp.user_playlist_create(user=user_id, name=f"{date} BillBoard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
