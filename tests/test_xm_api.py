import pytest
import requests

BASE_URL = "https://swapi.dev/api/"
SEARCH = BASE_URL + "{path}?search={name}"


@pytest.mark.parametrize("path, name",
                         [("films", "A New Hope")])
def test_film_by_name(path, name):
    api_uri = SEARCH.format(path=path, name=name)
    resp = requests.get(api_uri).json()
    film = json_extract(resp, "title")
    assert film == name


@pytest.mark.parametrize("path, name",
                         [("people", "Biggs Darklighter")])
def test_character_by_name(path, name):
    api_uri = SEARCH.format(path=path, name=name)
    resp = requests.get(api_uri).json()
    person = json_extract(resp, "name")
    assert person == name


@pytest.mark.parametrize("path, name",
                         [("people", "Luke Skywalker")])
def test_find_starship(path, name):
    starship_class = []
    api_uri = SEARCH.format(path=path, name=name)
    luke = requests.get(api_uri).json()
    starships = json_extract(luke, "starships")
    for x in starships:
        starships_list = requests.get(x).json()
        starship_class.append(json_extract(starships_list, "starship_class"))
    assert "Starfighter" in starship_class


@pytest.mark.parametrize("search_people, search_film, first_pilot, second_pilot, film_name",
                         [("people", "films", "Biggs Darklighter", "Luke Skywalker", "A New Hope")])
def test_from_task(search_people, search_film, first_pilot, second_pilot, film_name):
    characters_in_film = {}
    film_uri = SEARCH.format(path=search_film, name=film_name)
    film = requests.get(film_uri).json()
    characters = json_extract(film, "characters")
    for x in characters:
        characters_list = requests.get(x).json()
        characters_in_film[json_extract(characters_list, "name")] = x
    biggs_starship = get_data(characters_in_film[first_pilot], "starships")[0]
    starship_class = get_data(biggs_starship, "starship_class")
    starfighter_crew = get_data(biggs_starship, "pilots")
    assert starship_class == "Starfighter"
    assert second_pilot in characters_in_film.keys()
    assert characters_in_film[second_pilot] in starfighter_crew


def get_data(data, search_criteria):
    return json_extract(requests.get(data).json(), search_criteria)


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
    if isinstance(values, list):
        return values[0]
    else:
        return values
