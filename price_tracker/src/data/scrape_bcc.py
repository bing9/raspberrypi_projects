from src.data.base import Product, BaseScraper
from bs4 import BeautifulSoup
import logging
import json

logger = logging.getLogger(__name__)

class BCCScraper(BaseScraper):
    locators = dict(
        product_search_result_locator = {'name':'div', 'attrs' : {'class':'lister-product'}},
        )

    def parse_one_product(self, product_bs4: BeautifulSoup) -> Product:
        meta_data = json.loads(product_bs4.find('script', attrs = {'class': 'js-analytics-data'}).text)
        try:
            price = meta_data.get('price', '0')
        except: 
            price = None
            logger.info("Price Failed")
        try:
            hidden_price = None
        except: 
            hidden_price = None
        try:
            original_price = None
        except:
            original_price = None
        try:
            provider_id = meta_data.get('id', '0')
        except:
            provider_id = None
            logger.info("Provider_id Failed")
        try:
            name = product_bs4.find('h3', attrs = {'class': 'h2'}).text
        except:
            logger.info("Name Failed")
        try:
            url = 'https://bcc.nl'+ product_bs4.find('a', attrs = {'class': 'lister-product__titlelink'}).attrs['href']
        except:
            logger.info("URL Failed")
        return Product(
            provider = 'bcc',
            provider_id = provider_id,
            name = name,
            url = url,
            price = price,
            original_price = original_price,
            hidden_price = hidden_price
        )


