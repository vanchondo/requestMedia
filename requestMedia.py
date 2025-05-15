import configparser
import logging

import requests


def request_movies(url, moviesToRequest, pagesToSearch):
    ids = []
    page = 1
    headers = {
        'X-Api-Key': API_KEY,
        'content-type': 'application/json'
    }

    while page < pagesToSearch and len(ids) < moviesToRequest:
        params = {
            'page': page
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            movies_json = response.json()

            popular_movies = movies_json["results"]
            for movie in popular_movies:
                if len(ids) < moviesToRequest and movie.get("mediaInfo") == None and movie.get("adult") == False and movie.get("mediaType") == "movie":
                    ids.append(movie['id'])

        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")

        page+=1

    for media_id in ids:
        try:
            data = {
                "mediaId": media_id,
                "mediaType": "movie",
                "is4k": False,
                "serverId": 0,
                "profileId": 1,
                "rootFolder": "/movies",
                "userId": 1,
                "tags": []
            }

            response = requests.post(REQUEST_API_URL + '/request', headers=headers, json=data)

            if response.status_code == 201:
                logging.info(f"Request successful for media ID: {media_id}")
            else:
                logging.error(f"Request failed for media ID: {media_id} with status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e} for media ID: {media_id}")


# Read configuration from application.properties
config = configparser.ConfigParser()
config.read('application.properties')

API_KEY = config.get('Default', 'apiKey')
SERVICE_URL = config.get('Default', 'serviceUrl')
REQUEST_API_URL = SERVICE_URL + "/api/v1"
DISCOVER_PATH = REQUEST_API_URL + "/discover"

MOVIES_TO_REQUEST = 10
PAGES_TO_SEARCH = 100

request_movies(DISCOVER_PATH + '/movies', MOVIES_TO_REQUEST, PAGES_TO_SEARCH)
request_movies(DISCOVER_PATH + '/trending', MOVIES_TO_REQUEST, PAGES_TO_SEARCH)
request_movies(DISCOVER_PATH + '/movies/upcoming', MOVIES_TO_REQUEST, PAGES_TO_SEARCH)