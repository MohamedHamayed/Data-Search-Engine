""" module for images extracting """

import requests
from bs4 import BeautifulSoup

def scrape_images(company_name: str, product: str) -> list:
    """ request to google and get links of images """
    # string for search input
    search_prompt = f"{company_name}+{product}".replace(" ", "+")
    # url for requesting with input
    url = ("https://www.google.com/" +
           f"search?q={search_prompt}" +
           "&sxsrf=APwXEddCVh0F3LrhQ7i5EKf6nTNboFIzgw:1684519320663&tbm=isch")
    # list of links to images, returning value
    image_links = []
    # making a request
    request = requests.get(url, timeout=3).text
    # soup a response
    soup = BeautifulSoup(request, "lxml")
    # getting all img tags
    results = soup.find_all("img")

    # now we need to check if link is a url
    # if It is then adding to resulting list
    for result in results:
        image_link = result["src"]
        if "https" in image_link:
            image_links.append(image_link)

    return image_links[0]
