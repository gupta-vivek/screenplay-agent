from sentence_transformers import SentenceTransformer

from src.utils import get_lancedb_table, get_movie_list, fuzzy_match_title
from src.config import EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)

# Movie List
movie_list = get_movie_list()
movie_titles = {el: el.lower() for el in movie_list.keys()}

# Lancedb Table
table = get_lancedb_table()


def check_movie_exists(movie_title: str) -> str:
    """
    Checks if a given movie exists in the movie list by performing a fuzzy match on the movie title.

    :param str movie_title: Original movie title.
    :return: The fuzzy matched title.
    """
    fuzzy_movie = fuzzy_match_title(movie_title.lower(), movie_titles)
    if fuzzy_movie and movie_list[fuzzy_movie[-1]]:
        return fuzzy_movie[-1]
    return "The movie does not exist in the database."


def retrieve_documents(title: str, text_query: str, k: int = 3) -> list | str:
    """
    Retrieves a list of document texts based on the given movie title and text query.

    :param str title: Movie title returned by check_movie_exists function.
    :param str text_query: The textual content or query to match with the database.
    :param int k: The maximum number of documents to return.
    :return: A list of top k documents that match the query.
    """
    vector_query = model.encode(text_query)
    results = \
        table.search(query_type="hybrid").where(f"title='{title}'", prefilter=True).limit(k).vector(vector_query).text(
            text_query).to_pandas()['text'].to_list()
    if not results:  # ChatDeepSeek can't handle empty lists
        return "No results found."
    return results
