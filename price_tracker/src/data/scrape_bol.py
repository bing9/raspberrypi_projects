from src.data.base import BaseSearchProductParser, BaseScraper
import logging

logger = logging.getLogger(__name__)

class BolSearchProductParser(BaseSearchProductParser):
    @property
    def price(self):    
        try:
            price_int = self.product_bs4.find('span', attrs = {'data-test': 'price'}).contents[0].strip()
            price_frac = self.product_bs4.find('sup', attrs = {'data-test': 'price-fraction'}).contents[0].strip().strip('-')
            self._price = '.'.join([price_int, price_frac])
        except: 
            self._price = None
            logger.info("Price Failed")
        return self._price

    @property
    def hidden_price(self):
        try:
            self._hidden_price = self.product_bs4.find('meta', attrs = {'itemprop': 'price'}).attrs['content']
        except: 
            self._hidden_price = None
        return self._hidden_price

    @property
    def original_price(self):
        try:
            self._original_price = self.product_bs4.find('del', attrs = {'data-test': 'from-price'}).contents[0]
        except:
            self._original_price = None
        return self._original_price
    
    @property
    def provider_id(self):
        try:
            self._provider_id = self.product_bs4.attrs['data-id']
        except:
            self._provider_id = None
            logger.info("Provider_id Failed")
        return self._provider_id
    
    @property
    def name(self):
        try:
            product_meta = self.product_bs4.find('a', attrs = {'class': 'product-title'})
            self._name = product_meta.contents[0]
        except:
            logger.info("Name Failed")
        return self._name

    @property
    def url(self):
        try:
            product_meta = self.product_bs4.find('a', attrs = {'class': 'product-title'})
            self._url = 'https://bol.com'+ product_meta.attrs['href']
        except:
            logger.info("URL Failed")
        return self._url
    
    @property
    def provider(self):
        return 'bol'

class BolScraper(BaseScraper):
    locators = dict(
        product_search_result_locator = {'name':'li', 'attrs' : {'class': 'product-item--row'}},
        )

    @property
    def Parser(self):
        return BolSearchProductParser
