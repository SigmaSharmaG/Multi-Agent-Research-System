from langchain.tools import tool
import requests
from dotenv import load_dotenv
import os
from tavily import TavilyClient
from rich import print
from bs4 import BeautifulSoup
from readability import Document
import trafilatura
import requests
from urllib.parse import urlparse


load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query:str) -> str:
    """Search the web for recent and reliable information on a topic. Return Titles, URLs"""

    results = tavily.search(query=query,max_results=5)
    # print(results)
    out = []

    for r in results['results']:
        print(r['url'])
        out.append(f"Title : {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n")


    return "\n----\n".join(out)


@tool
def scrape_url(url: str) -> str:
    """Scrape readable text content from a webpage URL."""

    # Validate URL
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        return "Error: Please provide a valid HTTP or HTTPS URL."

    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=10,
            allow_redirects=True
        )

        response.raise_for_status()

        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unnecessary elements
        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "noscript"
        ]):
            tag.decompose()

        # Extract readable text
        text = soup.get_text(separator=" ", strip=True)

        # Limit output size
        return text[:10000] if text else "No readable text found."

    except requests.RequestException as e:
        return f"Error scraping URL: {e}"
