from pytube import Playlist
import youtube_dl

pl = Playlist("https://www.youtube.com/channel/UCo1qRcO1OehgkOD_fHsu_uQ/videos")

url = pl.parse_links()
print(len(url))




