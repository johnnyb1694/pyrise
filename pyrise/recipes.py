"""
Contains functionality to retrieve and process recipes sourced from: 
https://developer.edamam.com/edamam-docs-recipe-api
"""

import requests
import random


def get_recipes(
    app_id: str,
    app_key: str,
    min_calories: int = 400,
    max_calories: int = 800,
    fodmap: bool = True,
    n: int | None = 3
) -> dict:
    """
    Retrieves `n` random (or all, if unspecified) recipes from the `edamam` API service.

    Returns the recipe title and URL.

    Args:
        app_id (str): application key
        app_key (str): API key
        min_calories (int): minimum number of calories
        max_calories (int): maximum number of calories
        fodmap (bool): indicates whether recipes should conform to FODMAP standards or not
        n (int | None, optional): optionally controls the number of recipes. Defaults to None.
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
        subset = random.sample(range(len(hits)), n)
        hits = [hits[idx] for idx in subset]
    recipes = [hit["recipe"] for hit in hits]
    recipe_meta = [{"title": recipe["label"], "url": recipe["url"]} for recipe in recipes]
    return recipe_meta


if __name__ == '__main__':
    pass