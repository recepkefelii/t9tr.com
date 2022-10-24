from pytube import YouTube
from celery import Celery
import urllib.parse
app = Celery('tasks', broker='redis://localhost:6379')


# Youtube video downloader script
@app.task
def getMp3(urls):
    youtubeUrl=YouTube(urls)
    video=youtubeUrl.streams.filter(only_audio=True,abr="160kbps").first()

    video.download("./media",filename=f"{youtubeUrl.title}.mp3")
    
    query = youtubeUrl.title
    parse = urllib.parse.quote(query)
    print(query)
    result = f"https://t9tr.com/download/media/{parse}.mp3"
    return result

@app.task
def video(urls):
    youtubeUrl = YouTube(urls)
    query = youtubeUrl.title
    parse = urllib.parse.quote(query)
    videos = youtubeUrl.streams.filter(only_video=True, resolution='1080p').first()
    videos.download("./media",filename=f"{youtubeUrl.title}.mp4")
    result = f"https://t9tr.com/download/media/{parse}.mp4"
    return result


