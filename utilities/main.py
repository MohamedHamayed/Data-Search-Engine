
from collections import Counter
from utilities.tools import get_website
from utilities.wiki_scraper import scrape_wikipedia
from utilities.clearbit_scraper import scrape_clearbit
from utilities.linkedin_scraper import scrape_linkedin
from utilities.chatgpt import extract_products, extract_keywords
from utilities.img_scraper import scrape_images

import os
from dotenv import load_dotenv

load_dotenv()
CLEARBIT_KEY = os.getenv('CLEAR_BIT_KEY')
LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL')
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
OPENAI_KEY = os.getenv('OPEN_AI_KEY')

class Company():
    """ Company we need to find """

    def __init__(self, info: dict) -> None:
        self.name = info['name']
        self.country = info['country']
        self.website = info.get('url', None)

def process_request(info):
    """
    Logic is next: we taking a dict with companies
    it looks like { "company_name" : "name, "company_country" :... }
    then iterating throught it to apply script's algo for every company
    in future versions we will use another way for inputting data
    because it's not efficient now and useful only for testing
    """
    
    global CLEARBIT_KEY
    global LINKEDIN_EMAIL
    global LINKEDIN_PASSWORD
    global OPENAI_KEY

    # every company is an object
    company = Company(info)
    
    # search linkedin for company's page to scrape data
    print(f"Searching {company.name} linkedin page")
    linkedin_data = scrape_linkedin(company.name, company.country, company.website, LINKEDIN_EMAIL, LINKEDIN_PASSWORD)

    if not company.website:
        company.website = linkedin_data.get('companyPageUrl', None)
        print('linkedin', company.website)

    if not company.website:
        links = []
        for _ in range(3):
            link = get_website(company.name)
            links.append(link)
        
        counter = Counter(links)
        company.website = max(counter, key=counter.get)
        print('bing', company.website)

    # search wikipedia for company's page to scrape data
    print(f"Searching {company.name} wikipedia page")
    wiki_data = scrape_wikipedia(company.name, company.website, company.country)
    
    # if company don't have page on wiki we will get "False"
    # if "False" we need to scrape company's website if it exists
    if not wiki_data:
        wiki_data = scrape_wikipedia(company.name, company.website, "England")

    # search clearbit for company's page to scrape data
    print(f"Searching {company.name} clearbit page")
    try:
        clearbit_data = scrape_clearbit(company.website, CLEARBIT_KEY)
    except:
        clearbit_data = {}

    if wiki_data:
        prodcuts_services = extract_products(wiki_data, OPENAI_KEY)
        keywords = clearbit_data.get('tags',[])
        if len(keywords) == 0:
            keywords = extract_keywords(wiki_data, OPENAI_KEY)[:-1]
    else:
        prodcuts_services = extract_products(str(clearbit_data.get('description','')) + str(linkedin_data.get('description', '')), OPENAI_KEY)
        keywords = clearbit_data.get('tags',[])
        if len(keywords) == 0:
            keywords = extract_keywords(str(clearbit_data.get('description','')) + str(linkedin_data.get('description', '')), OPENAI_KEY)
    
    company_classification = {'naicsCode':clearbit_data.get('category',{}).get('naicsCode',''),
                              'naics6Codes':clearbit_data.get('category',{}).get('naics6Codes',[]),
                              'sicCode':clearbit_data.get('category',{}).get('sicCode',''),
                              'sic4Codes':clearbit_data.get('category',{}).get('sic4Codes',[])}

    if len(prodcuts_services['Products']):
        images = list(set([scrape_images(company.name, product) for product in prodcuts_services['Products']]))
    else:
        images = []

    return {"Products / Services":prodcuts_services, 'Keywords':keywords, 'Company Classification':company_classification, 'Images':images}