from pytube import YouTube
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379')


# Youtube video downloader script
@app.task
def getMp3(urls):
    youtubeUrl=YouTube(urls)
    video=youtubeUrl.streams.filter(only_audio=True,abr="160kbps").first()

    video.download("./media",filename=f"{youtubeUrl.video_id}.mp3")
    
    
    result = f"https://t9tr.com/download/media/{youtubeUrl.video_id}.mp3"
    return result

@app.task
def video(urls):
    youtubeUrl = YouTube(urls)
    videos = youtubeUrl.streams.filter(only_video=True, resolution='1080p').first()
    videos.download("./media",filename=f"{youtubeUrl.video_id}.mp4")
    result = f"https://t9tr.com/download/media/{youtubeUrl.video_id}.mp4"
    return result


