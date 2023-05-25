import clearbit
import tldextract

def scrape_clearbit(website, CLEARBIT_KEY):
    clearbit.key = CLEARBIT_KEY

    ext = tldextract.extract(website)
    company = clearbit.Company.find(domain=ext.domain+"."+ext.suffix)

    if company != None and 'pending' not in company:
        return dict(company)
    
    return {}