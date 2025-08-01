import requests
from bs4 import BeautifulSoup
from typing import List, Tuple, Optional
from urllib.parse import urljoin
import re
from Helpers import Email

error_handler = Email.ErrorHandler()


def story_scraper(url: str) -> List[Tuple[str, str]]:
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, "html.parser")

        items = soup.select(
            "section > div:nth-of-type(1) > div:nth-of-type(3) > ul > li"
        )
        story_data: List[Tuple[str, str]] = []
        for li in items:
            h2 = li.find("h2")
            if not h2:
                continue
            a = h2.find("a")
            if not a or not a.get("href"):
                continue

            title = a.get_text(strip=True)
            full_url = urljoin(url, a["href"])
            story_data.append((title, full_url))

        return story_data

    except requests.RequestException as e:
        if error_handler:
            error_handler.handle_error(f"[scrape_story_links] {e}")
        raise


def get_story_content(story_url: str) -> Optional[str]:
    try:
        resp = requests.get(story_url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, "html.parser")

        content_div = soup.select_one(
            "section > div:nth-of-type(1) > div:nth-of-type(3) > div:nth-of-type(2)"
        )
        if not content_div:
            return None

        full_text = content_div.get_text(separator=" ", strip=True)
        cleaned = re.sub(r"\s+", " ", full_text)

        summary = cleaned[:200]
        last_space = summary.rfind(" ")
        if last_space != -1:
            summary = summary[:last_space]
        return summary + "..."

    except requests.RequestException as e:
        if error_handler:
            error_handler.handle_error(f"[get_story_content] {e}")
        raise
