from price_tracker.src.data.scrape_bol import *
import pytest

def test_bolscraper():
    s = BolScraper('bol.com')
    print(s)