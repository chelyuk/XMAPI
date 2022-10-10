import json
from http import HTTPStatus

import pytest
import requests

BASE_URL = "https://swapi.dev/api/"
SEARCH = BASE_URL + "{path}?search={name}"


@pytest.mark.parametrize("path, name",
                         [("films", "A New Hope")])
def test_film_by_name(path, name):
    api_uri = SEARCH.format(path=path, name=name)
    resp = json.loads(requests.get(api_uri).text)
    film = json_extract(resp, "title")[0]
    assert film == name


@pytest.mark.parametrize("path, name",
                         [("people", "Biggs Darklighter")])
def test_character_by_name(path, name):
    api_uri = SEARCH.format(path=path, name=name)
    resp = json.loads(requests.get(api_uri).text)
    person = json_extract(resp, "name")[0]
    characters = json_extract(resp, "characters")
    print(characters)
    assert person == name


@pytest.mark.parametrize("path, name",
                         [("people", "Luke Skywalker")])
def test_find_starship(path, name):
    starship_class = []
    api_uri = SEARCH.format(path=path, name=name)
    luke = json.loads(requests.get(api_uri).text)
    starships = json_extract(luke, "starships")[0]
    for x in starships:
        starships_list = json.loads(requests.get(x).text)
        starship_class.append(json_extract(starships_list, "starship_class"))
    assert ["Starfighter"] in starship_class


@pytest.mark.parametrize("search_people, search_film, first_pilot, second_pilot, film_name",
                         [("people", "films", "Biggs Darklighter", "Luke Skywalker", "A New Hope")])
def test_from_task(search_people, search_film, first_pilot, second_pilot, film_name):
    starship_class = []
    characters_in_film = {}
    film_uri = SEARCH.format(path=search_film, name=film_name)
    film = json.loads(requests.get(film_uri).text)
    characters = json_extract(film, "characters")[0]
    for x in characters:
        characters_list = json.loads(requests.get(x).text)
        characters_in_film[json_extract(characters_list, "name")[0]] = x
    biggs_starship = json_extract(json.loads(requests.get(characters_in_film[first_pilot]).text), "starships")[0][0]
    starship_class = json_extract(json.loads(requests.get(biggs_starship).text), "starship_class")[0]
    starfighter_crew = json_extract(json.loads(requests.get(biggs_starship).text), "pilots")[0]
    assert starship_class == "Starfighter"
    assert second_pilot in characters_in_film.keys()
    assert characters_in_film[second_pilot] in starfighter_crew


def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == key:
                    arr.append(v)
                elif isinstance(v, (dict, list)):
                    extract(v, arr, key)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values
