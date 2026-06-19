from ddgs import DDGS
import requests
from bs4 import BeautifulSoup

def fetch_page(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        return text[:1000]
    except Exception as e:
        print(f"\nError: {e}\n")

def search(query):
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))

    if not results:
        return "No results found."

    formatted = ""
    for r in results:
        formatted += f"Title: {r['title']}\n"
        formatted += f"URL: {r['href']}\n"
        page_text = fetch_page(r['href'])
        if page_text:
            formatted += f"Content: {page_text}\n\n"
        else:
            formatted += f"Summary: {r['body']}\n\n"

    return formatted