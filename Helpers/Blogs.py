from bs4 import BeautifulSoup
import requests
from typing import List, Tuple, Optional
import re
from urllib.parse import urljoin
import Email as email


def scrape_articles(url: str) -> List[Tuple[str, str]]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.find_all("li")
        article_data = []

        for article in articles:
            h2_tag = article.find("h2")
            if h2_tag:
                title_tag = h2_tag.find("a")
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    article_url = urljoin(url, title_tag["href"])
                    article_data.append((title, article_url))

        return article_data

    except requests.RequestException as e:
        email.send(f"Error fetching articles from {url}: {e}")
        return []


def get_blog_content(blog_url: str) -> Optional[Tuple[str, str]]:
    try:
        response = requests.get(f"{blog_url}")
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        blog_name = soup.find("meta", property="og:title")["content"]
        blog_content_div = soup.find("div", itemprop="articleBody")
        blog_content = (
            blog_content_div.get_text(separator="\n")
            if blog_content_div
            else "Content not found"
        )

        return blog_name, blog_content

    except requests.RequestException as e:
        email.send(f"Error fetching blog content from {blog_url}: {e}")
        return None


def clean_content(content: str) -> str:
    cleaned = re.sub(r"\s+", " ", content)
    return cleaned.strip()
