import requests
from django.conf import settings
from gazpacho import Soup


def get_html(url):
    """
    Get HTML code of a page by its URL, using an external scraping provider.
    :param url: URL to get
    :return: The scraped HTML
    """
    payload = {"url": url}

    headers = {
        'x-api-key': settings.SCRAPING_ANT_API_KEY,
        'content-type': "application/json",
        'accept': "application/json"
    }

    resp = requests.post("https://api.scrapingant.com/v1/general", json=payload, headers=headers)

    if not resp.ok:
        raise requests.RequestException(
            f"There was a problem with the request ({resp.status_code}): {resp.content.decode()}"
        )

    return resp.content.decode()


def get_thing_soup(thing_id):
    """
    Get the page of a thing from Thingiverse.
    :param thing_id: ID of thing on Thingiverse
    :return: The 'Soup' of the page
    """
    url = f"https://www.thingiverse.com/thing:{thing_id}"
    html = get_html(url)
    return Soup(html)
