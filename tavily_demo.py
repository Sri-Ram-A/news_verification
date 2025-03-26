from tavily import TavilyClient
import os
from dotenv import load_dotenv
from pprint import pprint
load_dotenv("api.key")
API_KEY = os.getenv("TAVILY_API")

def getTavilySearchResults(query: str):
    tavily_client = TavilyClient(api_key=API_KEY)
    response = tavily_client.search(query, search_depth="advanced")
    print(response)

    finalRes = ""
    for result in response.get("results"):
        finalRes += result["content"] + "\n"

    everyRes = []
    for res in response.get("results"):
        if 'quora' not in res.get('url') or 'facebook' not in res.get('url') or 'instagram' not in res.get('url') or 't.me' not in res.get('url'):
            everyRes.append(res)

    return everyRes, finalRes

if __name__ == "__main__":
    pprint(getTavilySearchResults("Who is Narendra Modi?"))