from src.data.base import BaseSearchProductParser, Product, BaseScraper
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class MediaMarktSearchProductParser(BaseSearchProductParser):
    @property
    def price(self):
        try:
            prices = self.product_bs4.find('div', attrs = {'class': 'price', 'class': 'small'})
            self._price = ''.join([i.contents[0] for i in prices.contents]).strip().strip('-').replace(',', '.')
        except: 
            self._price = None
            logger.info("Price Failed")
        return self._price
    
    @property
    def original_price(self):
        try:
            old_prices = self.product_bs4.find('div', attrs = {'class': 'price-old', 'class': 'price'})
            self._original_price = ''.join([i.contents[0] for i in old_prices.contents]).strip().strip('-').replace(',', '.')
        except:
            self._original_price = None
        return self._original_price
    
    @property
    def provider_id(self):
        try:
            self._provider_id = self.product_bs4.attrs['data-reco-pid']
        except:
            self._provider_id = None
            logger.info("Provider_id Failed")
        return self._provider_id
    
    @property
    def name(self):
        try:
            self._name = self.product_bs4.find('img').attrs['alt']
        except:
            self._name = None
            logger.info("Name Failed")
        return self._name
    
    @property
    def url(self):
        try:
            self._url = 'https://mediamarkt.nl'+ self.product_bs4.find('a').attrs['data-clickable-href']
        except:
            self._url = None
            logger.info("URL Failed")
        return self._url
    
    @property
    def provider(self):
        return 'mediamarkt'

class MediaMarktScraper(BaseScraper):
    locators = dict(
        product_search_result_locator = {'name':'div', 'attrs' : {'class':'product-wrapper'}},
        )

    @property
    def Parser(self):
        return MediaMarktSearchProductParser




