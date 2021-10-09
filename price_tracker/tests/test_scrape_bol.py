from src.data.scrape_bol import *
import pytest
from bs4 import BeautifulSoup

@pytest.fixture
def scraper():
    url = 'https://www.bol.com/nl/nl/s/?searchtext=philips+sonicare'
    scraper = BolScraper(url)
    return scraper

@pytest.mark.webtest
def test_bolscraper():
    scraper = BolScraper('http://www.bol.com')
    soup = scraper.page
    assert isinstance(soup, BeautifulSoup)

@pytest.mark.webtest
def test_productlist(scraper):
    pl = scraper.get_productlist()
    assert len(pl) >= 20
    assert len(pl) <= 30

def test_product_correct(scraper):
    product = scraper.productlist[1]
    assert product.provider_id.startswith('920')
