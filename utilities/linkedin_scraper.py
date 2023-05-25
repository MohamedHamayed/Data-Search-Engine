""" Linkedin's API Access module """
import re
from linkedin_api import Linkedin
import requests
import fake_useragent
from bs4 import BeautifulSoup
import pycountry
from utilities.tools import fuzzy_sort, is_matched

ua = fake_useragent.FakeUserAgent()

def extract_id(url: str) -> str:
    """ Clean url to get company's id """
    company_id = re.search(r"company\/([^\/?]+)", url).group(1)
    return company_id


def get_company_id(company_name: str, country: str, max_retries=3, current_retry=0) -> str:
    """ Get company's linkedin ID for requesting linkedin_api """ 
    # making a search request to bing and extracting url from result
    # for request will be better to use simple formatting of company's name
    company_name = company_name.replace(" ", "+").lower()
    # making a string for request
    url = f"https://www.bing.com/search?q=get+{company_name}+{country}+linkedin+id+"
    search_results = requests.get(
        url, headers={"User-Agent": ua.safari}, timeout=3).text

    soup = BeautifulSoup(search_results, "lxml")
    # getting url from first result of search
    urls = [url.text for url in soup.find_all('cite') if '.linkedin.com/company' in url.text]

    if len(urls) == 0 and current_retry+1 < max_retries:
        get_company_id(company_name, country, max_retries=max_retries, current_retry=current_retry+1)

    # clean url to extract only company's id
    companies_ids = [extract_id(url) for url in urls]
    return companies_ids

def scrape_linkedin(company_name: str, country: str, website: str, LINKEDIN_EMAIL: str, LINKEDIN_PASSWORD: str) -> dict:
    """ Get info about company from linkedin api """
    api = Linkedin(LINKEDIN_EMAIL, LINKEDIN_PASSWORD)

    # to make an api request we need company's id from linkedin
    companies_ids =list(set(get_company_id(company_name, country)))

    if len(companies_ids) == 0:
        return {}

    companies_ids = fuzzy_sort(company_name, companies_ids)[:5]

    results = []
    for company_id in companies_ids:
        try:
            print(company_id)
            results.append(api.get_company(company_id))
        except:
            pass
    
    for index, result in enumerate(results.copy()):
        if website and result.get('companyPageUrl', None):
            if is_matched(website, [result['companyPageUrl']]):
                print('url match found')
                return result
            else:
                del results[index]
    
    for result in results:
        try:
            country_code = pycountry.countries.search_fuzzy(country)[0].alpha_2
        except:
            country = country.split(" ")[-1]
            country_code = pycountry.countries.search_fuzzy(country)[0].alpha_2
        
        hq_code = result.get('headquarter', {}).get('country', '')
        if hq_code == country_code:
            print('country hq match found')
            return result
        else:
            locations = result.get('confirmedLocations', [])
            for location in locations:
                if location.get('country', '') == country_code:
                    print('country cl match found')
                    return result

    print(len(results))
    if len(results):
        return results[0]
    return {}