
from typing import Union
from pydantic import BaseModel
import uvicorn
import json
import requests
from fastapi import FastAPI, Response, Request, Form
from fastapi.templating import Jinja2Templates
from utilities.main import process_request

class CompanyInfo(BaseModel):
    name: str
    country: str
    url: Union[str, None] = None

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get('/healthz')
def healthz_func(): 
    '''
    Health check for API server.
    '''
    return Response(content='\n', status_code=200, media_type='text/plain')

@app.post("/extract_info")
def predict(company_info:CompanyInfo):
    req = company_info.dict()
    
    try:
        result = process_request(req)
    except:
        result = {"Products / Services":{"Products":[],"Services":[]}, 'Keywords':[], 'Company Classification':{'naicsCode':'','naics6Codes':[],'sicCode':'','sic4Codes':[]}, 'Images':[]}    

    response = Response(content=json.dumps(result), status_code=200, media_type='application/json')
    
    return response

@app.get("/")
def main(request: Request):
    """ homepage """

    return templates.TemplateResponse("index.html", {"request": request, "api": None})

@app.post('/search')
def search_company(request: Request, company: str = Form(...), country: str = Form(...), url: str = Form(None)):
    """ Making a request with inputs from form """
    input_data = dict()
    input_data['name'] = company
    input_data['country'] = country
    input_data['url'] = url

    api_url = 'http://localhost:8080/extract_info'
    context = requests.post(api_url, json=input_data).json()
    print(context)
    
    return templates.TemplateResponse("index.html",{"request": request, "api": context, "input_data": input_data})

if __name__ =="__main__":
    uvicorn.run(app , host='0.0.0.0', port=8080)
