from src.data.base import Product, BaseScraper
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class BolScraper(BaseScraper):
    locators = dict(
        product_search_result_locator = {'name':'li', 'attrs' : {'class': 'product-item--row'}},
        )
    def parse_one_product(self, product_bs4: BeautifulSoup) -> Product:
        product_meta = product_bs4.find('a', attrs = {'class': 'product-title'})
        try:
            price_int = product_bs4.find('span', attrs = {'data-test': 'price'}).contents[0].strip()
            price_frac = product_bs4.find('sup', attrs = {'data-test': 'price-fraction'}).contents[0].strip().strip('-')
            price = '.'.join([price_int, price_frac])
        except: 
            price = None
            logger.info("Price Failed")
        try:
            hidden_price = product_bs4.find('meta', attrs = {'itemprop': 'price'}).attrs['content']
        except: 
            hidden_price = None
        try:
            original_price = product_bs4.find('del', attrs = {'data-test': 'from-price'}).contents[0]
        except:
            original_price = None
        try:
            provider_id = product_bs4.attrs['data-id']
        except:
            provider_id = None
            logger.info("Provider_id Failed")
        try:
            name = product_meta.contents[0]
        except:
            logger.info("Name Failed")
        try:
            url = 'https://bol.com'+ product_meta.attrs['href']
        except:
            logger.info("URL Failed")
        return Product(
            provider = 'bol',
            provider_id = provider_id,
            name = name,
            url = url,
            price = price,
            original_price = original_price,
            hidden_price = hidden_price
        )


