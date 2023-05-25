""" Wikipedia Scraper """

from bs4 import BeautifulSoup
import requests
from utilities.multiwiki import WP_CODES
from utilities.tools import (is_matched,
                             get_wiki_links,
                             cleanhtml)

def scrape_wikipedia(name: str, website: str, country: str) -> str:
    """ Function for getting company's data from wikipedia """
    # First check if there a wp-code for this country
    wpcode = None
    for wikicode in WP_CODES.keys():
        if country.lower() in wikicode.lower():
            wpcode = WP_CODES[wikicode]

    if wpcode is None:
        wpcode = "en"
        country = "England"

    # replacing whitespace to use it for api request
    formatted_name = name.replace(" ", "_")

    # url for request to wiki api
    url = f"https://{wpcode}.wikipedia.org/api/rest_v1/page/html/{formatted_name}"

    # requesting data from wiki's api
    wiki_page = requests.get(url, timeout=3)
    
    # variable with splitted company's name
    name_split = formatted_name.split('_')

    # if can't find page, algo will try to delete last word
    # needs because sometimes name contains to much words for wiki's search
    if wiki_page.status_code == 404:
        # deleting words until they'll end with loop
        while len(name_split) > 1:
            # pop last word from company's name
            name_split.pop()

            # recursion to use all combinations
            return scrape_wikipedia(" ".join(name_split), website, country)

        return ""
    # if page exists we need to validate this page
    # if page is really about company then parse data
    else:
        soup = BeautifulSoup(wiki_page.text, "lxml")
        # <p> tags contains info we need
        info = soup.find_all('p')
        
        # var for saving non-cleaned data
        dirty_data = ""
        
        # getting all company's website urls from wikipedia
        # all_wiki_websites = list with urls
        all_wiki_websites = get_wiki_links(url, country)

        if all_wiki_websites is None:
            return dirty_data

        # need to check if urls on wiki and from search the same
        # if they not the same, it can be only because of wrong wiki page
        # and it means that company don't have wiki page with 99% accuracy
        if is_matched(website, all_wiki_websites) is False:
            return dirty_data

        # if all ok, return to parsing data
        # this loop will create one string with full text from all p elements of page
        for element in info:
            dirty_data += str(element)

        # cleaning string from html tags and words like '[example]', [201], [39]
        cleaned_data = cleanhtml(dirty_data)

        return cleaned_data
