from src.data.base import Product, ProductList, BaseScraper
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

# class BolLocator(BaseLocator):
#     product_list_locator = {'li', attrs = {'class': 'product-item--row'}}

class BolScraper(BaseScraper):
    def get_productlist(self) -> ProductList:
        self._productlist_bs4 = self.page.find_all('li', attrs = {'class': 'product-item--row'})
        productlist = ProductList()
        for i in self._productlist_bs4:
            try:
                productlist.append(self.parse_one_product(i))
            except:
                logger.info(f"Skipped! Parsing product {i.attrs['data-id']} failed")
        return productlist

    def parse_one_product(self, product_bs4: BeautifulSoup) -> Product:
        product_meta = product_bs4.find('a', attrs = {'class': 'product-title'})
        try:
            price_int = product_bs4.find('span', attrs = {'data-test': 'price'}).contents[0].strip()
            price_frac = product_bs4.find('sup', attrs = {'data-test': 'price-fraction'}).contents[0].strip()
            price_frac = '00' if price_frac=='-' else price_frac
            price = '.'.join([price_int, price_frac])
        except: 
            price = None
            logger.info("Price Failed")
        try:
            hidden_price = product_bs4.find('meta', attrs = {'itemprop': 'price'}).attrs['content']
        except: 
            hidden_price = None
            logger.info("Hidden Price Failed")
        try:
            original_price = product_bs4.find('del', attrs = {'data-test': 'from-price'}).contents[0]
        except:
            original_price = None
            logger.info("Original Price not exits")
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


