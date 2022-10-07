from django.urls import path
from .views import urlname,download,procces,procces2

urlpatterns = [
    path('log/',urlname,name='log'),
    path('video/',download,name='video'),
    path('music/',procces,name='music'),
    path('nomusic/',procces2,name='nomusic'),
]
