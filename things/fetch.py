import json
from concurrent.futures import ThreadPoolExecutor

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

    json_response = json.loads(resp.content.decode())
    return json_response["content"]


def get_thing_soup(thing_id):
    """
    Get the page of a thing from Thingiverse.
    :param thing_id: ID of thing on Thingiverse
    :return: The 'Soup' of the page with summary, and the 'Soup' of the page with downloads
    """
    base_url = f"https://www.thingiverse.com/thing:{thing_id}"
    downloads_url = f"https://www.thingiverse.com/thing:{thing_id}/files"
    with ThreadPoolExecutor(max_workers=2) as executor:
        base_future = executor.submit(get_html, base_url)
        downloads_future = executor.submit(get_html, downloads_url)
    base_html = base_future.result()
    downloads_html = downloads_future.result()
    return Soup(base_html), Soup(downloads_html)


def get_thing_details(thing_id):
    """
    Get the details of a thing from Thingiverse.
    :param thing_id: ID of thing on Thingiverse
    :return: A dict containing details of the thing
    """
    soup, downloads_soup = get_thing_soup(thing_id)
    title = soup.find("div", {"class": "ThingPage__modelName"}, mode="first").text
    summary = soup.find("div", {"class": "ThingPage__description"}, mode="first").html
    print_settings = soup.find("div", {"class": "ThingPage__preHistory"}, mode="all")

    print_parts = "".join(part.html for part in print_settings)
    description = f"{summary}{print_parts}"

    image_carousel = soup.find("div", {"class": "ThingImageCarousel__carouselWrapper"}, mode="first")
    image_items = image_carousel.find("li", {"class": "slide"})
    images = []
    for item in image_items:
        img_src = item.find("img").attrs["src"]
        if img_src.find("img.youtube.com") > -1:
            iframe_src = item.find("iframe").attrs["src"]
            if iframe_src.startswith("//www"):
                iframe_src = iframe_src.replace("//www", "https://www")
            images.append(iframe_src)
        else:
            images.append(img_src)

    file_links = downloads_soup.find("a", {"class": "ThingFile__download"}, mode="all")
    files = [link.attrs["href"] for link in file_links]

    return {
        "title": title,
        "description": description,
        "images": images,
        "files": files,
    }
