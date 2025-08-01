from bs4 import BeautifulSoup
import requests
from typing import List, Tuple, Optional
import re
from urllib.parse import urljoin, urlparse, parse_qs
from Helpers import Email

error_handler = Email.ErrorHandler()
BASE_URL = "https://www.islamweb.net/ar/articles/46/أخلاق-وتزكية"


def clean_content(content: str) -> str:
    return re.sub(r"\s+", " ", content).strip()


def scrape_articles_on_page(page: int) -> List[Tuple[str, str]]:
    url = f"{BASE_URL}?pageno={page}"
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, "html.parser")

    items = soup.select("section > div:nth-of-type(1) > div:nth-of-type(3) ul li")
    results = []
    for li in items:
        a = li.select_one("h2 > a")
        if a and (href := a.get("href")):
            title = a.get_text(strip=True)
            link = urljoin(url, href)
            results.append((title, link))
    return results


def scrape_articles(url: str) -> List[Tuple[str, str]]:
    # Parse pageno from URL, default=1
    qs = parse_qs(urlparse(url).query)
    page = int(qs.get("pageno", ["1"])[0])
    try:
        return scrape_articles_on_page(page)
    except Exception as e:
        error_handler.handle_error(f"[Page {page}] scrape failed: {e}")
        return []


def get_blog_content(blog_url: str) -> Optional[Tuple[str, str]]:
    resp = requests.get(blog_url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, "html.parser")

    # Title
    h2 = soup.select_one(
        "section > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > h2"
    )
    title = h2.get_text(strip=True) if h2 else "No Title"

    # Content container
    content_div = soup.select_one(
        "section > div:nth-of-type(1) > div:nth-of-type(3) > div:nth-of-type(2)"
    )
    if not content_div:
        content = "Content not found"
    else:
        parts = []
        for node in content_div.find_all(["p", "img"]):
            if node.name == "p":
                text = node.get_text(strip=True)
                if text:
                    parts.append(clean_content(text))
            elif node.name == "img" and (src := node.get("src")):
                parts.append(f"[Image] {urljoin(blog_url, src)}")
        content = "\n\n".join(parts)

    return title, content
