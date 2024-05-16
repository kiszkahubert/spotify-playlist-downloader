import googleapiclient.discovery
import spotipy
import os

from spotipy.oauth2 import SpotifyOAuth
from pytube import YouTube

def get_playlist_info(spotify_playlist_url):
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope="playlist-modify-private",
            redirect_uri="https://localhost:3000",
            client_id=os.getenv('client-spotify-id'),
            client_secret=os.getenv('client-spotify-secret'),
            show_dialog=True,
            cache_path="token.txt"))
    all_songs = {}
    playlist = sp.playlist(spotify_playlist_url)
    for item in playlist['tracks']['items']:
        song_name = item['track']['name']
        artist_name = item['track']['artists'][0]['name']
        all_songs[song_name] = artist_name
    return all_songs

def get_music_link(song_name,song_artist):
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.getenv('youtube-developer-key')

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY
    )
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=song_name+" "+song_artist
    )
    response = request.execute()
    video_id = response['items'][0]['id']['videoId']
    return f"https://www.youtube.com/watch?v={video_id}"
def link_mp3_download(link):
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path='.')
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file,new_file)
    print(yt.title + " has been successfully downloaded.")


if __name__ == "__main__":
    if os.path.exists("token.txt"):
        os.remove('token.txt')
    playlist_link = input("Please insert link to playlist you want to download: ")
    all_songs = get_playlist_info(playlist_link)
    for song_name, song_artist in all_songs.items():
        link = get_music_link(song_name, song_artist)
        link_mp3_download(link)