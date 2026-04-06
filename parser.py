from typing import Optional, List, Dict

from bs4 import BeautifulSoup


def parse_title(html: Optional[str]) -> str:
    if not html:
        return "No title"

    soup = BeautifulSoup(html, 'lxml')
    title_tag = soup.find('title')

    if title_tag and title_tag.text:
        return title_tag.text.strip()

    return "No title"


def parse_links(html: Optional[str]) -> List[Dict[str, str]]:
    if not html:
        return []

    soup = BeautifulSoup(html, 'lxml')
    links = []

    for a_tag in soup.find_all('a'):
        href = a_tag.get('href')
        text = a_tag.get_text(strip=True)

        if href:
            links.append({
                'text': text if text else 'No text',
                'href': href
            })

    return links
