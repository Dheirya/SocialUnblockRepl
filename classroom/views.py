from django.http import JsonResponse
from django.views.decorators.cache import cache_page, never_cache
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import WebVTTFormatter
from django.http import HttpResponse
from youtubesearchpython import *
from django.shortcuts import render
import uyts
import vimeo
import requests
import pytube


v = vimeo.VimeoClient(
    token='e33822544fd675d2f15b953a05111009',
    key='d6f25ff10f9e140a827782b649ed145b0ce9b48b',
    secret='LCsvT3FhVvz9EQiV2n4FAStq/21QbufTDC3rxGLzxQnyNsFB38KaAAXMNOXh7dEav76T2GYof6Sp3zLJn45mVScpPYp8QFwDe3RkuwSlHSzNydouN+DNDokul/kRpyCI'
)


@cache_page(60 * 60 * 24)
def YoutubeSearchJSON(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            if request.GET.get('minify'):
                search = uyts.Search(query)
                return JsonResponse(search.resultsJSON, safe=False, json_dumps_params={'indent': 2})
            else:
                search = uyts.Search(query)
                return JsonResponse(search.resultsJSON, safe=False)
        else:
            return render(request, 'classroom/index.html')


@cache_page(60 * 5)
def YoutubeAdvancedSearchJSON(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            if request.GET.get('minify'):
                search = VideosSearch(query, limit=500)
                return JsonResponse(search.result(), safe=False, json_dumps_params={'indent': 2})
            else:
                search = VideosSearch(query, limit=500)
                return JsonResponse(search.result(), safe=False)
        else:
            return JsonResponse([{'Error': 'No Query'}], safe=False)


@never_cache
def YoutubeGetVideoSRC(request):
    if request.method == 'GET':
        yo_id = request.GET.get('id')
        if yo_id:
            youtube = pytube.YouTube('https://youtube.com/watch?v=' + yo_id)
            return JsonResponse([{'src': youtube.streams.get_highest_resolution().url}], safe=False, json_dumps_params={'indent': 2})
        else:
            return JsonResponse([{'Error': 'No Query'}], safe=False)


@cache_page(60 * 60 * 24)
def YoutubeGetVideoTrack(request):
    if request.method == 'GET':
        yo_id = request.GET.get('id')
        if yo_id:
            transcript = YouTubeTranscriptApi.get_transcript(yo_id)
            formatter = WebVTTFormatter()
            json_formatted = formatter.format_transcript(transcript)
            return HttpResponse(json_formatted, content_type="text/vtt")
        else:
            return JsonResponse([{'Error': 'No Query'}], safe=False)


@cache_page(60 * 5)
def YoutubeVideoDetailJSON(request):
    if request.method == 'GET':
        youtube_id = request.GET.get('id')
        if youtube_id:
            if request.GET.get('minify'):
                try:
                    videoInfo = Video.getInfo('https://youtu.be/' + youtube_id, mode=ResultMode.json)
                    return JsonResponse(videoInfo, safe=False, json_dumps_params={'indent': 2})
                except:
                    return JsonResponse([{'Error': 'No Comments'}], safe=False)
            else:
                try:
                    videoInfo = Video.getInfo('https://youtu.be/' + youtube_id, mode=ResultMode.json)
                    return JsonResponse(videoInfo, safe=False)
                except:
                    return JsonResponse([{'Error': 'No Comments'}], safe=False)
        else:
            return JsonResponse([{'Error': 'No Query'}], safe=False)


@cache_page(60 * 5)
def YoutubeUserVideosDetailJSON(request):
    if request.method == 'GET':
        youtube_id = request.GET.get('id')
        if youtube_id:
            if request.GET.get('minify'):
                try:
                    videoInfo = Playlist(playlist_from_channel_id(youtube_id))
                    return JsonResponse(videoInfo.videos, safe=False, json_dumps_params={'indent': 2})
                except:
                    return JsonResponse([{'Error': 'No Comments'}], safe=False)
            else:
                try:
                    videoInfo = Playlist(playlist_from_channel_id(youtube_id))
                    return JsonResponse(videoInfo.videos, safe=False)
                except:
                    return JsonResponse([{'Error': 'No Comments'}], safe=False)
        else:
            return JsonResponse([{'Error': 'No Query'}], safe=False)


@cache_page(60 * 60 * 24)
def YoutubeCommentsSearchJSON(request):
    if request.method == 'GET':
        youtube_id = request.GET.get('id')
        if youtube_id:
            if request.GET.get('minify'):
                try:
                    comments = requests.get('https://www.googleapis.com/youtube/v3/commentThreads?key=AIzaSyDFO7M1HRjsSIuovZkKoexorn4_SDswAdk&textFormat=plainText&part=snippet&maxResults=50&order=relevance&videoId=' + youtube_id)
                    return JsonResponse(comments.json(), safe=False, json_dumps_params={'indent': 2})
                except:
                    return JsonResponse([{'Error': 'No Comments'}], safe=False)
            else:
                try:
                    comments = requests.get('https://www.googleapis.com/youtube/v3/commentThreads?key=AIzaSyDFO7M1HRjsSIuovZkKoexorn4_SDswAdk&textFormat=plainText&part=snippet&maxResults=50&order=relevance&videoId=' + youtube_id)
                    return JsonResponse(comments.json(), safe=False)
                except:
                    return JsonResponse([{'Error': 'No Comments'}], safe=False)
        else:
            return JsonResponse([{'Error': 'No Query'}], safe=False)


@cache_page(60 * 5)
def VimeoSearchJSON(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        limit = request.GET.get('num')
        if query:
            if request.GET.get('minify'):
                if limit:
                    search = v.get('/videos?page=1&per_page=' + limit + '&query=' + query + '&sort=likes')
                    return JsonResponse(search.json(), safe=False, json_dumps_params={'indent': 2})
                else:
                    search = v.get('/videos?page=1&per_page=10&query=' + query + '&sort=likes')
                    return JsonResponse(search.json(), safe=False, json_dumps_params={'indent': 2})
            else:
                if limit:
                    search = v.get('/videos?page=1&per_page=' + limit + '&query=' + query + '&sort=likes')
                    return JsonResponse(search.json(), safe=False)
                else:
                    search = v.get('/videos?page=1&per_page=10&query=' + query + '&sort=likes')
                    return JsonResponse(search.json(), safe=False)
        else:
            return JsonResponse([{'Error': 'No Query'}], safe=False)


@cache_page(60 * 5)
def DailyMotionSearchJSON(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        limit = request.GET.get('num')
        if query:
            if request.GET.get('minify'):
                if limit:
                    search = requests.get('https://api.dailymotion.com/videos?fields=id,embed_url,thumbnail_url,title,owner.screenname,duration&limit=' + limit + '&search=' + query)
                    return JsonResponse(search.json(), safe=False, json_dumps_params={'indent': 2})
                else:
                    search = requests.get('https://api.dailymotion.com/videos?fields=id,embed_url,thumbnail_url,title,owner.screenname,duration&limit=50&search=' + query)
                    return JsonResponse(search.json(), safe=False, json_dumps_params={'indent': 2})
            else:
                if limit:
                    search = requests.get('https://api.dailymotion.com/videos?fields=id,embed_url,thumbnail_url,title,owner.screenname,duration&limit=' + limit + '&search=' + query)
                    return JsonResponse(search.json(), safe=False)
                else:
                    search = requests.get('https://api.dailymotion.com/videos?fields=id,embed_url,thumbnail_url,title,owner.screenname,duration&limit=50&search=' + query)
                    return JsonResponse(search.json(), safe=False)
        else:
            return JsonResponse([{'Error': 'No Query'}], safe=False)
