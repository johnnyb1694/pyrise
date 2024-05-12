"""Contains functionality to retrieve and process recipes.

Ultimate source: https://developer.edamam.com/edamam-docs-recipe-api
"""
import requests
import random


def _sample_hits(
    hits: dict,
    n: int
) -> list[dict]:
    """Randomly samples extracted hits (recipes).

    Args:
        hits (dict): list of recipes that were produced by the API response
        n (int): number of articles to extract
    """
    indices = random.sample(range(len(hits)), n)
    random_subset = [hits[idx] for idx in indices]
    return random_subset


def _extract_recipes(
    hits: dict
) -> list[dict]:
    """Extracts the recipe elements of each 'hit' and filters fields on recipe title and URL.

    Args:
        hits (dict): list of recipes that were produced by the API response
    """
    recipes = [hit["recipe"] for hit in hits]
    recipes_short = [{"title": recipe["label"], "url": recipe["url"]} for recipe in recipes]
    return recipes_short


def get_recipes(
    app_id: str,
    app_key: str,
    min_calories: int = 400,
    max_calories: int = 800,
    fodmap: bool = True,
    n: int | None = 3
) -> list[dict]:
    """Retrieves `n` random (or all, if unspecified) recipes from the `edamam` API service.

    Args:
        app_id (str): application key
        app_key (str): API key
        min_calories (int): minimum number of calories
        max_calories (int): maximum number of calories
        fodmap (bool): indicates whether recipes should comply with FODMAP standards or not
        n (int | None, optional): optionally controls the number of recipes. Defaults to `3`.
    """
    params = {
        "type": "public",
        "app_id": app_id,
        "app_key": app_key,
        "diet": "balanced",
        "health": ("fodmap-free" if fodmap else None),
        "calories": f"{min_calories}-{max_calories}"
    }
    response = requests.get(
        url="https://api.edamam.com/api/recipes/v2",
        params=params
    )
    deserialised = response.json()
    hits = deserialised["hits"]
    if n:
        hits = _sample_hits(hits, n)
    recipes = _extract_recipes(hits)
    return recipes


if __name__ == '__main__':
    pass