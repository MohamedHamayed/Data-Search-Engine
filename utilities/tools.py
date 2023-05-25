""" 
Toolkit of useful functions for application includes
* cleanhtml - deletes all html tags from text
* format_url - standartize url addresses
* is_matched - checking if urls matching
* get_wiki_links - scrape company's links from wiki
"""

import re
import time
import requests
from bs4 import BeautifulSoup
import fake_useragent
import tldextract
from fuzzywuzzy import fuzz
from utilities.multiwiki import WEBSITE

ua = fake_useragent.UserAgent()

def cleanhtml(raw_html: str) -> str:
    """ Delete all html tags from text """
    cleantext = re.sub('<.*?>', '', raw_html)
    cleantext = re.sub(r'\[\d+\]', ' ', cleantext)
    return cleantext

def is_matched(website: str, other_sites: list) -> bool:
    """ Check for url match between search's and wikipedia's links """
    ext = tldextract.extract(website)
    website = ext.domain+"."+ext.suffix

    for site in other_sites:
        ext = tldextract.extract(str(site))
        site = ext.domain+"."+ext.suffix

        if site.lower().strip() == website.lower().strip():
            return True
    return False


def get_wiki_links(url: str, country: str) -> list:
    """ 
    Get company website links from wikipedia
    Need for validating wiki page
    """
    response = requests.get(url, timeout=3).text
    soup = BeautifulSoup(response, 'lxml')
    search_string = WEBSITE[country]
    result = []

    item = soup.find("th", string=search_string)
    if item is not None:
        item = item.parent.find_all("a")
    else:
        return item

    for tag in item:
        result.append(tag['href'])

    return result

def get_website(name: str) -> str:
    """ Using bing's search to find company's url """
    name = name.replace(" ", "+")
    url = f"https://www.bing.com/search?q=get+the+{name}+official+website"
    search_page = requests.get(
        url, headers={"User-Agent": ua.safari}, timeout=3).text

    soup = BeautifulSoup(search_page, "lxml")
    dirty_address = soup.find("cite")

    clean_address = cleanhtml(str(dirty_address))

    time.sleep(1)

    return clean_address

def fuzzy_sort(string, string_list):
    scores = [(fuzz.ratio(string, item), item) for item in string_list]
    scores.sort(reverse=True)  # Sort in descending order of fuzzy match scores
    sorted_list = [item for score, item in scores]
    return sorted_list
