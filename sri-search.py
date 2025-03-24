from googlesearch import search
from newspaper import Article
from serpapi import GoogleSearch
import pprint
API_KEY="5ee4136c602d451fd46aa04f03948041f84f9d574bc84b1d03cd4cec9312d9c3"
def extract_urls_from_image(url,api_key=API_KEY,hl='en',country="in"):
    params = {
    "api_key": api_key ,
    "engine": "google_lens",
    "url":url,
    "country":country,
    "hl":hl
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    urls = [dictionary["link"] for dictionary in results["visual_matches"]]
    return urls

def extract_urls_from_text_query(query:str,fact_checking=True):
    urls=list(search(query))
    if(fact_checking==True):
        sites="(site:factly.in OR site:boomlive.in OR site:snopes.com OR site:factcheck.org)"
        urls=urls+list(search(query+sites))
    else:
       return urls
  
def extract_content_from_url(url:str,source=None,is_text=False,is_image=False):
  article = Article(url)
  article.download()
  article.parse()
  import tldextract
  extracted = tldextract.extract(url)
  source = extracted.domain + '.' + extracted.suffix
  info={
        "url":url,
        "source":source,     
        "title":article.title,
        "authors":article.authors,#list of author names
        "publish_date":article.publish_date,#datetime object
        "top_image":article.top_image,#list of image urls
        "movies":article.movies,#list of video urls
        "text":article.text
    }
  if(is_image):
    info["media_type"]="image"

  if(is_text):
    info["media_type"]="text"

       
  return info

def extract_info_from_claims(claims: list, url=None, is_image=False, is_text=False):
    list_of_string = list()
    list_of_dictionary = list()
    list_of_list = list()
    
    temp_str = ""
    for claim in claims:
        if is_image:
            urls = extract_urls_from_image(url)
        if is_text:
            urls = extract_urls_from_text_query(claim)  # extract list of urls for a claim
        
        for url in urls:
            dictionary = extract_content_from_url(url)
            temp_str += f"Information from source: {dictionary['source']} published on {dictionary['publish_date']} titled: {dictionary['title']} has the following text: {dictionary['text']}\n"
            list_of_dictionary.append(dictionary)
        
        list_of_string.append(temp_str)  # Assuming you meant to append temp_str here
        list_of_list.append(list_of_dictionary)
        temp_str = ""
        list_of_dictionary = []
    
    return list_of_string, list_of_list


claims = [
   "1. Mahatma Gandhi lives on as India's Father of the Nation.",
    "2. Mahatma Gandhi is still alive.",
    "3. Mahatma Gandhi is still leading mass movements."
]
print(extract_info_from_claims(claims, is_text=True))