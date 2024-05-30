"""Contains functionality to retrieve stoic quotes

Ultimate source: https://stoic.tekloon.net/stoic-quote
"""
import requests


def get_stoic_quote() -> dict[str, str]:
    """Get a stoic quote for the daily email service
    """
    response = requests.get("https://stoic.tekloon.net/stoic-quote")
    return response.json()


if __name__ == '__main__':
    print(get_stoic_quote())
