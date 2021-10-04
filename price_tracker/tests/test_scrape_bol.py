from src.data.scrape_bol import *
import pytest
from bs4 import BeautifulSoup

@pytest.mark.webtest
def test_bolscraper():
    scraper = BolScraper('http://www.bol.com')
    soup = scraper.page
    assert isinstance(soup, BeautifulSoup)

@pytest.mark.webtest
def test_productlist():
    url = 'https://www.bol.com/nl/nl/s/?searchtext=philips+sonicare'
    scraper = BolScraper(url)
    pl = scraper.get_productlist()
    assert len(pl) >= 20
    assert len(pl) <= 30

def test_locator():
    pass
