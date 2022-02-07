from django.http import JsonResponse
from django.views.decorators.cache import cache_page, never_cache
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import WebVTTFormatter
from django.http import HttpResponse
from youtubesearchpython import *
from django.shortcuts import redirect
from django.shortcuts import render
from bs4 import BeautifulSoup
import uyts
import vimeo
import requests
import pytube
import json
import twint


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


@cache_page(60 * 60 * 6)
def YoutubeAdvancedSearchJSON(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        number = int(request.GET.get('number')) - 1
        if query:
            if request.GET.get('minify'):
                search = VideosSearch(query, limit=500)
                for _ in range(number):
                    search.next()
                return JsonResponse(search.result(), safe=False, json_dumps_params={'indent': 2})
            else:
                search = VideosSearch(query, limit=500)
                for _ in range(number):
                    search.next()
                return JsonResponse(search.result(), safe=False)
        else:
            return JsonResponse([{'Error': 'No Query'}], safe=False)


@never_cache
def YoutubeGetVideoSRC(request):
    if request.method == 'GET':
        yo_id = request.GET.get('id')
        if yo_id:
            youtube = pytube.YouTube('https://youtube.com/watch?v=' + yo_id)
            if request.GET.get('redirect'):
                return redirect(youtube.streams.get_highest_resolution().url)
            else:
                return JsonResponse([{'src': youtube.streams.get_highest_resolution().url}], safe=False)
        else:
            return JsonResponse([{'Error': 'No Query'}], safe=False)


@cache_page(60 * 60 * 24 * 30)
def YoutubeGetVideoTrack(request):
    if request.method == 'GET':
        yo_id = request.GET.get('id')
        if yo_id:
            try:
                transcript = YouTubeTranscriptApi.get_transcript(yo_id)
                formatter = WebVTTFormatter()
                json_formatted = formatter.format_transcript(transcript)
                return HttpResponse(json_formatted, content_type="text/vtt")
            except:
                json_formatted = """WEBVTT

00:00:00.000 --> 00:00:00.001
Loading...
                """
                return HttpResponse(json_formatted, content_type="text/vtt")
        else:
            return JsonResponse([{'Error': 'No Query'}], safe=False)


@cache_page(60 * 60 * 24 * 7)
def GoogleSearchAPI(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            search = requests.get('https://suggestqueries.google.com/complete/search?client=safari&q=' + query)
            json_search = search.text
            firstDelPos = json_search.find(',{"k"')
            secondDelPos = json_search.find('"}')
            stringAfterReplace = json_search.replace(json_search[firstDelPos + 1:secondDelPos], "").replace(',"}', '')
            return JsonResponse(json.loads(stringAfterReplace), safe=False)
        else:
            return JsonResponse([{'Error': 'No Query'}], safe=False)


@cache_page(60 * 60 * 6)
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


@cache_page(60 * 60 * 6)
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


@cache_page(60 * 60 * 24 * 14)
def YoutubeCommentsSearchJSON(request):
    if request.method == 'GET':
        youtube_id = request.GET.get('id')
        if youtube_id:
            if request.GET.get('minify'):
                try:
                    comments = requests.get('https://www.googleapis.com/youtube/v3/commentThreads?key=AIzaSyDFO7M1HRjsSIuovZkKoexorn4_SDswAdk&textFormat=plainText&part=snippet&maxResults=75&order=relevance&videoId=' + youtube_id)
                    return JsonResponse(comments.json(), safe=False, json_dumps_params={'indent': 2})
                except:
                    return JsonResponse([{'Error': 'No Comments'}], safe=False)
            else:
                try:
                    comments = requests.get('https://www.googleapis.com/youtube/v3/commentThreads?key=AIzaSyDFO7M1HRjsSIuovZkKoexorn4_SDswAdk&textFormat=plainText&part=snippet&maxResults=75&order=relevance&videoId=' + youtube_id)
                    return JsonResponse(comments.json(), safe=False)
                except:
                    return JsonResponse([{'Error': 'No Comments'}], safe=False)
        else:
            return JsonResponse([{'Error': 'No Query'}], safe=False)


@cache_page(60 * 60 * 6)
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


@cache_page(60 * 60 * 6)
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


@cache_page(60 * 60 * 24)
def TwitterSearchJSON(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        c = twint.Config()
        c.Search = query
        c.Limit = 125
        c.Pandas = True
        c.Popular_tweets = True
        likes = request.GET.get('likes')
        if not likes:
            c.Min_likes = 100
        twint.run.Search(c)
        df = twint.storage.panda.Tweets_df
        djson = df.to_json(orient='table')
        return HttpResponse(djson, content_type='application/json')


@cache_page(60 * 60 * 24 * 30)
def URLJSON(request):
    if request.method == 'GET':
        query = request.GET.get('id')
        try:
            response = requests.get(query, headers={"User-Agent": "Googlebot"})
            soup = BeautifulSoup(response.text, "html.parser")
            metas = soup.find_all('meta', {"name": "description"})
            title = soup.find_all('title')
            do = False
            ix = False
            for m in metas:
                if m.get('name') == 'description':
                    if do is False:
                        do = True
                        desc = m.get('content')
                        url_desc = desc
                else:
                    if do is False:
                        do = True
                        url_desc = ""
            for t in title:
                if ix is False:
                    ix = True
                    url_title = t.string
            return JsonResponse({"data": {"title": url_title, "description": url_desc}}, safe=False)
        except:
            return JsonResponse({'error': 'error'}, safe=False)
