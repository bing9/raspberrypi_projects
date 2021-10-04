from base import Product, ProductList, BaseScraper
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class BolScraper(BaseScraper):
    def get_productlist(self) -> ProductList:
        productlist_bs4 = self.page.find_all('li', attrs = {'class': 'product-item--row'})
        productlist = ProductList()
        for i in productlist_bs4:
            try:
                productlist.append(self.parse_one_product(i))
            except:
                logger.info(f"Skipped! Parsing product {i.attrs['data-id']} failed")
        return productlist

    def parse_one_product(self, product_bs4: BeautifulSoup) -> Product:
        product_meta = product_bs4.find('a', attrs = {'class': 'product-title'})
        try:
            price = product_bs4.find('meta', attrs = {'itemprop': 'price'}).attrs['content']
        except: 
            price = None
            logger.info("Price Failed")
        try:
            original_price = product_bs4.find('del', attrs = {'data-test': 'from-price'}).contents[0]
        except:
            original_price = None
            logger.info("Original Price Failed")
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
            original_price = original_price
        )


