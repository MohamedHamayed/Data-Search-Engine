
import openai
import json
from googletrans import Translator

translator = Translator()

def extract_products(sent, OPENAI_KEY, curr_retry=0, max_retries=3):
    openai.api_key = OPENAI_KEY

    try:
        trans_sent = translator.translate(sent[:3600]).text
        response = openai.Completion.create(
          model="text-davinci-003",
          prompt="""You are a highly intelligent and accurate Named-entity recognition(NER) system. You take Passage which is information about a company as input and your task is to recognize and extract specific types of named entities in that given passage and classify into a set of following predefined entity types:
          ['Products that are offered by the company', 'Services that are offered by the company']

          Your output format is only "{"Products": entity in the input text, "Services": entity in the input text}", form, no other form.

          Input: \'""" + trans_sent + """\'
          Output:""",
          temperature=0.7,
          max_tokens=200,
          top_p=1.0,
          frequency_penalty=0.0,
          presence_penalty=0.0
        )
        result = json.loads(response['choices'][0]['text'])
    except:
        curr_retry += 1
        if curr_retry < max_retries:
            return extract_products(sent, OPENAI_KEY, curr_retry=curr_retry, max_retries=max_retries)
        else:
            return {'Products':[], 'Services':[]}
    
    result['Products'] = [product.replace('and ', '', 1) if product.startswith('and ') else product for product in result['Products'].split(", ")]
    result['Services'] = [service.replace('and ', '', 1) if service.startswith('and ') else service for service in result['Services'].split(", ")]
    result['Services'] = [service for service in result['Services'] if len(service.split(" ")) < 5]
    return result


def extract_keywords(sent, OPENAI_KEY, curr_retry=0, max_retries=3):
    openai.api_key = OPENAI_KEY
    
    try:
        trans_sent = translator.translate(sent[:3600]).text
        response = openai.Completion.create(
          model="text-davinci-003",
          prompt="""You are a highly intelligent and accurate Keywords Extractor system. You take Passage which is information about a company as input and your task is to recognize and extract important keywords that are related to the company in that given passage.

          Your output format is only "Keywords: keyword in the input text, keyword in the input text, ...", form, no other form.

          Input: \'""" + trans_sent + """\'
          Output:""",
          temperature=0.5,
          max_tokens=60,
          top_p=1.0,
          frequency_penalty=0.8,
          presence_penalty=0.0
        )
        result = [keyword.replace('and ', '', 1) if keyword.startswith('and ') else keyword for keyword in response['choices'][0]['text'].split('Keywords: ')[-1].split(', ')]
    except:
        curr_retry += 1
        if curr_retry < max_retries:
            return extract_keywords(sent, OPENAI_KEY, curr_retry=curr_retry, max_retries=max_retries)
        else:
            return []
        
    return result