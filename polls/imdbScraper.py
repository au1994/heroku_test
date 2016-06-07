import logging
import sys
import traceback

import requests

from bs4 import BeautifulSoup


def get_search_results(movie):

    url = "http://www.imdb.com/find?s=tt&q=" + movie

    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        logging.info(e)
        traceback.print_exc(e)

    soup = BeautifulSoup(r.content, "html.parser")
    movies = soup.find_all("td", {"class": "result_text"})

    json_array = []

    if len(movies) == 0:
        json_object = {}
        json_object['Error'] = "No results found"
        return json_object

    for item in movies:
        if item is not None:
            title = item.get_text().strip()
            url = item.find("a").get("href")
            movie_id = url[7:16]
        url = "http://www.imdb.com" + url
        json_object = {}
        json_object['Title'] = title
        json_object['Url'] = url
        json_object['Id'] = movie_id
        json_array.append(json_object)

    return json_array


def get_movie_results(movie_id):

    url = "http://www.imdb.com/title/" + movie_id + "/?ref_=fn_al_tt_1"
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        logging.info(e)
        traceback.print_exc(e)

    soup = BeautifulSoup(r.content, "html.parser")
    movie_details = soup.find("div", {"class": "plot_summary"})
    json_array = []

    if movie_details is None:
        print "No results found"
        json_object = {}
        json_object['Error'] = "No results found"
        return json_object

    description = movie_details.find("div", {"class": "summary_text"})
    director = movie_details.find_all("span", {"itemprop": "director"})
    writer = movie_details.find_all("span", {"itemprop": "creator"})
    actor = movie_details.find_all("span", {"itemprop": "actors"})
    rating = soup.find("span", {"itemprop": "ratingValue"})
    title_details = soup.find("div", {"class": "title_wrapper"})
    title = title_details.find("h1", {"itemprop": "name"})
    duration = title_details.find("time", {"itemprop": "duration"})
    release_date = title_details.find("meta",
                                      {"itemprop": "datePublished"})

    genre = title_details.find_all("span", {"itemprop": "genre"})

    json_object = {}

    if title is not None:
        json_object['Title'] = title.get_text().strip()

    if duration is not None:
        json_object['Duration'] = duration.get_text().strip()

    if release_date is not None:
        json_object['ReleaseDate'] = release_date['content']

    if description is not None:
        json_object['Description'] = description.get_text().strip()

    if director is not None:
        directors = ""
        for item in director:
            directors = directors + item.get_text().strip() + ", "
        json_object['Directors'] = directors

    if genre is not None:
        genres = ""
        for item in genre:
            genres = genres + item.get_text().strip() + " "
        json_object['Genre'] = genres

    if writer is not None:
        writers = ""
        for item in writer:
            writers = writers + item.get_text().strip() + " "
        json_object['Writer'] = writers

    if actor is not None:
        actors = ""
        for item in actor:
            actors = actors + item.get_text().strip() + " "
        json_object['Actors'] = actors

    if rating is not None:
        json_object['Rating'] = rating.get_text().strip()

    return json_object
