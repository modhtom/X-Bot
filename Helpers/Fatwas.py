from Helpers import Email
from bs4 import BeautifulSoup
import requests
from typing import List, Tuple, Optional
import re
from urllib.parse import urljoin, urlparse, parse_qs

error_handler = Email.ErrorHandler()


def clean_content(content: str) -> str:
    return re.sub(r"\s+", " ", content).strip()


def scrape_articles(url: str) -> List[Tuple[str, str]]:
    qs = parse_qs(urlparse(url).query)
    page = int(qs.get("pageno", ["1"])[0])
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, "html.parser")

        items = soup.select("section > div:nth-of-type(1) > ul:nth-of-type(1) > li")
        results = []
        for li in items:
            a = li.find("a")
            if a and (href := a.get("href")):
                title = a.get_text(strip=True)
                full_url = urljoin(url, href)
                results.append((title, full_url))
        return results

    except Exception as e:
        error_handler.handle_error(f"[scrape_articles] page={page} failed: {e}")
        return []


def get_fatwa_content(fatwa_url: str) -> Optional[Tuple[str, str]]:
    try:
        resp = requests.get(fatwa_url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, "html.parser")

        question_paras = soup.select(
            "section > div:nth-of-type(1) > div > div:nth-of-type(2) > div:nth-of-type(3) > p"
        )
        question = next(
            (p.get_text(strip=True) for p in question_paras if p.get_text(strip=True)),
            "",
        )

        answer_div = soup.select_one(
            "section > div:nth-of-type(1) > div > div:nth-of-type(3) > div"
        )
        if not answer_div:
            answer = ""
        else:
            paras = [
                clean_content(p.get_text())
                for p in answer_div.find_all("p")
                if p.get_text(strip=True)
            ]
            answer = "\n\n".join(paras)

        return clean_content(question), clean_content(answer)

    except Exception as e:
        error_handler.handle_error(f"[get_fatwa_content] failed on {fatwa_url}: {e}")
        return None
