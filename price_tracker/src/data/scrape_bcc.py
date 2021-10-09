from src.data.base import BaseSearchProductParser, BaseScraper
import logging
import json

logger = logging.getLogger(__name__)

class BCCSearchProductParser(BaseSearchProductParser):
    @property
    def price(self):
        try:
            meta_data = json.loads(self.product_bs4.find('script', attrs = {'class': 'js-analytics-data'}).text)
            self._price = meta_data.get('price', '0')
        except:
            self._price = None
            logger.info("Price Failed")
        return self._price
    
    @property
    def original_price(self):
        try:
            self._original_price = self.product_bs4.find('span', attrs = {'class': 'priceblock__price', 'class':'priceblock__price--listprice'}).text.strip().strip('€').strip().strip('-').replace(',','.')
        except:
            self._original_price = None
        return self._original_price

    @property
    def provider_id(self):
        try:
            meta_data = json.loads(self.product_bs4.find('script', attrs = {'class': 'js-analytics-data'}).text)
            self._provider_id = meta_data.get('id', '0')
        except:
            self._provider_id = None
            logger.info("Provider_id Failed")
        return self._provider_id

    @property
    def name(self):
        try:
            self._name = self.product_bs4.find('h3', attrs = {'class': 'h2'}).text
        except:
            self._name = None
            logger.info("Name Failed")
        return self._name

    @property
    def url(self):
        try:
            self._url = 'https://bcc.nl'+ self.product_bs4.find('a', attrs = {'class': 'lister-product__titlelink'}).attrs['href']
        except:
            self._url = None
            logger.info("URL Failed")
        return self._url
    
    @property
    def provider(self):
        return 'bcc'

class BCCScraper(BaseScraper):
    locators = dict(
        product_search_result_locator = {'name':'div', 'attrs' : {'class':'lister-product'}},
        )

    @property
    def Parser(self):
        return BCCSearchProductParser
