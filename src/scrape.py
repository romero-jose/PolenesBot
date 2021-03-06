import time
import re
import requests
from enum import Enum, auto
from typing import Dict, List
from bs4 import BeautifulSoup


class Pollen(Enum):
    ARBOL = auto()
    PLATANO = auto()
    PASTO = auto()
    MALEZA = auto()
    TOTAL = auto()


URL = "http://polenes.cl/sitio/santiago.asp"
KEYWORDS: Dict[str, Pollen] = {
    "arbol": Pollen.ARBOL,
    "platano": Pollen.PLATANO,
    "oriental": Pollen.PLATANO,
    "maleza": Pollen.MALEZA,
    "pasto": Pollen.PASTO,
    "total": Pollen.TOTAL,
    "todos": Pollen.TOTAL,
}
FULL_NAMES: Dict[Pollen, str] = {
    Pollen.ARBOL: "total de árboles",
    Pollen.PLATANO: "de plátano oriental",
    Pollen.PASTO: "de pasto",
    Pollen.MALEZA: "de maleza",
    Pollen.TOTAL: "total",
}
TABLE_ORDER: List[Pollen] = [
    Pollen.ARBOL,
    Pollen.PLATANO,
    Pollen.PASTO,
    Pollen.MALEZA,
    Pollen.TOTAL,
]


def fetch_content() -> str:
    response = requests.get(URL)
    return response.text


def fetch_content_cached(prev_time=time.time(), cached=None) -> str:
    curr_time = time.time()
    if cached is None or curr_time - prev_time > 60:
        cached = fetch_content()
    prev_time = curr_time
    return cached


def scrape_content(content: str) -> Dict[Pollen, int]:
    soup = BeautifulSoup(content, "html.parser")
    rows = soup.find("table").find("table").find_all("tr")
    last_row = rows[-1]

    text = [col.get_text() for col in last_row]
    matches = map(lambda t: re.findall(pattern="[0-9]+", string=t), text)
    matches = filter(lambda l: l != [], matches)
    numbers = map(lambda m: int(m[0]), matches)
    polenes = dict(zip(TABLE_ORDER, numbers))
    polenes[Pollen.TOTAL] = sum(polenes.values())
    return polenes


def scrape_polenes() -> Dict[Pollen, int]:
    return scrape_content(fetch_content())
