import unittest

from src.scrape import *


class TestScrape(unittest.TestCase):
    def test_scrape_content(self):
        with open("test/assets/sample.html") as file:
            content = file.read()
        expected = {
            Pollen.ARBOL: 26,
            Pollen.PLATANO: 1,
            Pollen.PASTO: 4,
            Pollen.MALEZA: 4,
            Pollen.TOTAL: 35,
        }
        self.assertEqual(scrape_content(content), expected)
