import json
import os

import bs4
import lancedb
import requests
from dotenv import load_dotenv, find_dotenv


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


def get_lancedb_table():
    """
    Retrieve a LanceDB table based on the configuration specified in environment variables.

    :return: The LanceDB table object corresponding to the specified table name.
    """
    _ = load_dotenv(find_dotenv())

    # Lance DB
    uri = os.getenv("LANCEDB_URI")
    api_key = os.getenv("LANCEDB_API_KEY")
    region = os.getenv("LANCEDB_REGION")
    table_name = os.getenv("LANCEDB_TABLE_NAME")

    db = lancedb.connect(uri=uri, api_key=api_key, region=region)

    table = db.open_table(table_name)

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
