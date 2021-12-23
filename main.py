import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

spotipy_id = "your id"
spotipy_secret = "your authentication code"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=spotipy_id,
        client_secret=spotipy_secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]


date = input("which year do you want to travel to? type the date in this format YYYY-MM-DD:")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
response = response.text

playlist = sp.user_playlist_create(user=user_id,name=f"{date} Billboard 100",public=False)
print(playlist)
soup = BeautifulSoup(response, "html.parser")
songs = []
songs_url =[]
year = date.split("-")[0]
titles = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
for title in titles:
    songs.append(title.get_text())
for song in songs:
    result = sp.search(q=f"{song} {year}", type="track")
    try:
        url = result["tracks"]["items"][0]["uri"]
        songs_url.append(url)
    except IndexError:
        print(f"{song} not found")
sp.playlist_add_items(user=user_id, playlist_id=playlist["id"], tracks=songs_url)
