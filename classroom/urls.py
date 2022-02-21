from django.urls import path
from . import views

urlpatterns = [
    path('', views.YoutubeSearchJSON, name='youtube-json'),
    path('vimeo/', views.VimeoSearchJSON, name='vimeo-json'),
    path('youtube/', views.YoutubeAdvancedSearchJSON, name='youtube-advanced-json'),
    path('dailymotion/', views.DailyMotionSearchJSON, name='dailymotion-json'),
    path('youtube/comments/', views.YoutubeCommentsSearchJSON, name='youtube-comments-json'),
    path('youtube/details/', views.YoutubeVideoDetailJSON, name='youtube-detail'),
    path('youtube/channel/', views.YoutubeUserVideosDetailJSON, name='youtube-channel'),
    path('youtube/src/', views.YoutubeGetVideoSRC, name='youtube-src'),
    path('youtube/captions/', views.YoutubeGetVideoTrack, name='youtube-caption'),
    path('google/', views.GoogleSearchAPI, name='google'),
    path('twitter/', views.TwitterSearchJSON, name='twitter-search'),
    path('tweet/', views.TwitterDetailJSON, name='twitter-detail'),
    path('url/', views.URLJSON, name='url-json'),
    path('cache/', views.CacheBuster, name='cache-buster')
]
