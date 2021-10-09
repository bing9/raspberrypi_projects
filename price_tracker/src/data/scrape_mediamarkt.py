from src.data.base import Product, BaseScraper
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class MediaMarktScraper(BaseScraper):
    locators = dict(
        product_search_result_locator = {'name':'div', 'attrs' : {'class':'product-wrapper'}},
        )

    def parse_one_product(self, product_bs4: BeautifulSoup) -> Product:
        try:
            prices = product_bs4.find('div', attrs = {'class': 'price', 'class': 'small'})
            price = ''.join([i.contents[0] for i in prices.contents]).strip().strip('-').replace(',', '.')
        except: 
            price = None
            logger.info("Price Failed")
        try:
            hidden_price = None
        except: 
            hidden_price = None
            logger.info("Hidden Price Failed")
        try:
            old_prices = product_bs4.find('div', attrs = {'class': 'price-old', 'class': 'price'})
            original_price = ''.join([i.contents[0] for i in old_prices.contents]).strip().strip('-').replace(',', '.')
        except:
            original_price = None
            logger.info("Original Price not exits")
        try:
            provider_id = product_bs4.attrs['data-reco-pid']
        except:
            provider_id = None
            logger.info("Provider_id Failed")
        try:
            name = product_bs4.find('img').attrs['alt']
        except:
            logger.info("Name Failed")
        try:
            url = 'https://mediamarkt.nl'+ product_bs4.find('a').attrs['data-clickable-href']
        except:
            logger.info("URL Failed")
        return Product(
            provider = 'mediamarkt',
            provider_id = provider_id,
            name = name,
            url = url,
            price = price,
            original_price = original_price,
            hidden_price = hidden_price
        )


