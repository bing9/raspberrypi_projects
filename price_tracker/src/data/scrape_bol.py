from .scrape_base import Product, ProductList, BaseScraper
from bs4 import BeautifulSoup
import requests
from datetime import datetime

class BolScraper(BaseScraper):
    def get_productlist(self) -> ProductList:
        productlist_bs4 = self.page.find_all('li', attrs = {'class': 'product-item--row'})
        productlist = ProductList()
        for i in productlist_bs4:
            try:
                productlist.append(self.parse_one_product(i))
            except:
                print(f"Skipped! cannot parse product: {i.attrs}")
        return productlist

    def parse_one_product(self, product_bs4: BeautifulSoup) -> Product:
        product_meta = product_bs4.find('a', attrs = {'class': 'product-title'})
        try:
            price = product_bs4.find('meta', attrs = {'itemprop': 'price'}).attrs['content']
        except: 
            price = None
        try:
            original_price = product_bs4.find('del', attrs = {'data-test': 'from-price'}).contents[0]
        except:
            original_price = None
        return Product(
            provider = 'bol',
            provider_id = product_bs4.attrs['data-id'],
            name = product_meta.contents[0],
            url = 'https://bol.com'+ product_meta.attrs['href'],
            price = price,
            original_price = original_price,
            scrape_datetime = datetime.now()
        )


