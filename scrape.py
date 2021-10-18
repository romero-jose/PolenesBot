import re
import requests
from bs4 import BeautifulSoup


URL = 'http://polenes.cl/sitio/santiago.asp'
# POLENES = ['Total Árboles', 'Plátano Oriental', 'Pastos', 'Malezas']
KEYWORDS = ['arbol', 'platano', 'pasto', 'maleza']
FULL_NAMES = {
    'arbol': 'total de árboles',
    'platano': 'plátano oriental',
    'pastos': 'pasto',
    'maleza': 'maleza',
}


def scrape_polenes(url=URL):
    site = requests.get(url)
    soup = BeautifulSoup(site.content, "html.parser")
    rows = soup.find('table') \
               .find('table') \
               .find_all('tr')
    last_row = rows[-1]

    text = [col.get_text() for col in last_row]
    matches = map(lambda t: re.findall(pattern='[0-9]+', string=t), text)
    matches = filter(lambda l: l != [], matches)
    numbers = map(lambda m: int(m[0]), matches)
    polenes = dict(zip(KEYWORDS, numbers))

    return polenes
