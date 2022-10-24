
from rest_framework.response import Response
from rest_framework.decorators import api_view,throttle_classes
from rest_framework import status
from rest_framework.request import Request
import re
from .models import url
from .serializers import UrlSerializer
from api.tasks import getMp3,video
from ytvideo.celery import app
from pytube import YouTube 
from hurry.filesize import size
import time
from celery.result import AsyncResult
from rest_framework.throttling import AnonRateThrottle



class ytDowloader():
    def __init__(self,url):
        self.url = url

    
    def geturl(self):
        yt = YouTube(self.url)
        name = yt.title 
        productSchema = {
                    "name" : None ,
                    "thumbnail" : None,
                    "author" : None,
                    "length" : None,
                    "view" : None,}

        videoSchema = {

        }

        productSchema["name"] = yt.title
        productSchema["thumbnail"] = yt.thumbnail_url
        productSchema["author"] = yt.author
        productSchema["length"] = time.strftime("%H:%M:%S", time.gmtime(yt.length))
        productSchema["view"] = yt.views

        dvideos = yt.streams.filter(progressive=True, resolution='360p')
        for d in dvideos:
            videoSchema["video360"] = ({
            "download":d.url,
            "size":size(d.filesize),
            "quality":d.resolution,
            "format":d.audio_codec,
            "videoic":d.includes_video_track,
            "tur":'Video'

                    })

        
        cvideos = yt.streams.filter(progressive=True, resolution='720p')
        for c in cvideos:
            videoSchema["video720"] = ({
            "download":c.url,
            "size":size(c.filesize),
            "quality":c.resolution,
            "format":c.audio_codec,


                    })
        cvideos = yt.streams.filter(only_audio=True,)
        for c in cvideos:
            videoSchema["music"] = ({
            "size":size(d.filesize),
            "quality":c.abr,
            "format":c.audio_codec,
            "videoic":c.includes_video_track,

                    })
        cvideos = yt.streams.filter(only_video=True, resolution='1080p')
        for c in cvideos:
            videoSchema["video1080"] = ({
            "size":size(c.filesize),
            "quality":c.resolution,
            "format":c.audio_codec,
            "videoic":c.includes_video_track,

                    })
        
        videoSchema["infoVideo"] = productSchema




        return videoSchema



def youtube_url_validation(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, url)

    return youtube_regex_match








        

@api_view(['GET'])
def urlname(request:Request):
    if request.method == 'GET':
        data = url.objects.all()
        serializer = UrlSerializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)



@api_view(['POST'])
@throttle_classes([AnonRateThrottle])
def download(request:Request):
    global ytdowload
    data = request.data
    urls  = ytDowloader(url=data['url'])
    serializer = UrlSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        response = {
            'info':"successful",
            'data':urls.geturl()
        }

        return Response(response,status=status.HTTP_201_CREATED)
    
    return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST','GET'])
def procces(request:Request):
    if request.method == 'POST':                        
        data = request.data

        result = getMp3.delay(data['url'])
        response = {
            "id": result.id,
        }
        return Response(data=response,status=status.HTTP_201_CREATED)
    
    elif request.method == 'GET': 
        celeryWorkerId = request.query_params['id']
        reponse = app.AsyncResult(celeryWorkerId).get()
    
        return Response(data=reponse)


@api_view(['POST','GET'])
def procces2(request:Request):
    if request.method == 'POST':
        data = request.data
        if youtube_url_validation(url=data['url']):
            result = video.delay(data['url'])
            response = {
                "id": result.id
            }
            return Response(data=response,status=status.HTTP_201_CREATED)
        else:
            return Response(data={'please enter youtube video URL'})
    
    elif request.method == 'GET':
        celery = request.query_params['id']
        response = app.AsyncResult(celery).get()
        return Response(data=response)


    


