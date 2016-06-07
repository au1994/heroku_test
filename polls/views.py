import json
import pdb
import sys
import traceback

import requests

import imdbScraper

from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def search_movie(request):

    movie = request.GET.get('q', '')
    movie_list = imdbScraper.get_search_results(movie)

    if type(movie_list) is dict:
        data = json.dumps(movie_list)
        return HttpResponse(data,
                            content_type='application/json',
                            status=404)

    paginator = Paginator(movie_list, 20)
    page = request.GET.get('page')

    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(1)

    # print type(movies)
    movies = movies.object_list
    data = json.dumps(movies)

    return HttpResponse(data,
                        content_type='application/json',
                        status=200)


def exact_movie(request):

    movie_id = request.GET.get('q', '')
    data = imdbScraper.get_movie_results(movie_id)
    if 'Error' in data:
        status_code = 404
    else:
        status_code = 200
    data = json.dumps(data)
    return HttpResponse(data,
                        content_type='application/json',
                        status=status_code)
