import json
import os
from rapidfuzz import process
import bs4
import lancedb
import requests
from src import config


def get_all_movies() -> list[str]:
    """
    Get a list of all movies from imsdb.
    :return: List of movie titles
    """

    all_scripts_url = "https://imsdb.com/all-scripts.html"
    page = requests.get(all_scripts_url)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')
    movie_p = soup.find_all('p')
    movie_titles = [p.find('a').text for p in movie_p]

    return movie_titles


def convert_title_to_url(title: str) -> str:
    """
    Convert movie title to imsdb url.
    :param str title: Movie title
    :return: Movie url
    """
    title = title.replace(' ', '-')
    title = title.replace(':', '')
    return f"https://imsdb.com/scripts/{title}.html"


def get_script(script_url: str) -> str | None:
    """
    Fetch script content from a given URL.

    :param str script_url: URL of the script to fetch
    :return: The extracted script text as a string
    """
    page = requests.get(script_url)
    if page.status_code != 200:
        print(f"No Script Found for {script_url}")
        return None

    soup = bs4.BeautifulSoup(page.content, 'html.parser')
    td_tag = soup.find('td', class_='scrtext')
    return td_tag.text


def get_lancedb_table() -> lancedb.db.Table:
    """
    Retrieve a LanceDB table

    :return: The LanceDB table
    """
    db = lancedb.connect(uri=config.LANCEDB_URI, api_key=config.LANCEDB_API_KEY, region=config.LANCEDB_REGION)
    table = db.open_table(config.LANCEDB_TABLE_NAME)
    return table


def get_movie_list() -> dict:
    """
    Retrieves the list of movies.

    :return:
    """
    project_directory = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..'))  # Directory of the current script
    data_file = os.path.abspath(os.path.join(project_directory, "data/movie_list.json"))

    with open(data_file, 'r') as f:
        movie_list = json.load(f)
    return movie_list


def fuzzy_match_title(user_input: str, titles: dict, threshold: int = 80) -> tuple | None:
    """
    Compares a user-input string with a list of possible titles.

    :param str user_input: The input string entered by the user for matching.
    :param dict titles: A dictionary containing potential titles to match against the input.
    :param int threshold: The minimum similarity score at which a match is considered valid.
    :return: The best matching title from the list.
    """
    match = process.extractOne(user_input, titles, score_cutoff=threshold)
    return match if match else None
