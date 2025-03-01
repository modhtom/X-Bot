import Email as email
from bs4 import BeautifulSoup
import requests
from typing import List, Tuple, Optional
import re
from urllib.parse import urljoin


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


def get_fatwa_content(fatwa_url: str) -> Optional[Tuple[str, str]]:
    try:
        response = requests.get(fatwa_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Find (Question) section
        question_text = ""
        div_main = soup.find("div", class_="mainitem quest-fatwa")
        if div_main:
            title_element = div_main.find("h3", class_="mainitemtitle2")
            title = (
                title_element.get_text(strip=True)
                if title_element
                else "No title found"
            )
            question_element = div_main.find("div", itemprop="text")
            question_text = (
                question_element.get_text(strip=True).replace("\n", " ")
                if question_element
                else "No question text found"
            )
        # Find (Answer) section
        answer_div = soup.find(
            "div", class_="mainitem quest-fatwa", itemprop="acceptedAnswer"
        )
        answer_text = ""
        if answer_div:
            answer_content = answer_div.find("div", itemprop="text")
            if answer_content:
                answer_text = answer_content.get_text(strip=True)

        return clean_content(question_text), clean_content(answer_text)

    except requests.RequestException as e:
        email.send(f"Error fetching fatwa content from {fatwa_url}: {e}")
        return None


def clean_content(content: str) -> str:
    cleaned = re.sub(r"\s+", " ", content)
    return cleaned.strip()
