import requests
from bs4 import BeautifulSoup
from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import shutil
from typing import Optional
from selenium import webdriver
import logging

logger = logging.getLogger(__name__)

class ProductList(list):
    def save_prices_to_db(self, path: Path):
        file_name = datetime.now().strftime("%Y-%m-%d %I:%M%p")
        headers = ['provider', 'provider_id', 'name', 'price', 'original_price','hidden_price','URL']
        to_save_data = ['\t'.join(headers)+'\n'] + [p.to_records()+'\n' for p in self]
        raw_location = path/f"{file_name}.tsv"
        old_file_location = path.parent/'external'/'old_price.tsv'
        new_file_location = path.parent/'external'/'new_price.tsv'
        if to_save_data:
            with open(raw_location, 'w') as file:
                file.writelines(to_save_data)
            # save for faster access
            shutil.copy(new_file_location, old_file_location)
            shutil.copy(raw_location, new_file_location)

@dataclass
class Product:
    provider: str
    provider_id: str
    name: str
    url: str
    price: str
    original_price: str
    hidden_price : Optional[str]

    def to_records(self):
        return '\t'.join([
                    self.provider if self.provider else '', 
                    self.provider_id if self.provider_id else '', 
                    self.name  if self.name else '', 
                    self.price  if self.price else '', 
                    self.original_price  if self.original_price else '',
                    self.hidden_price  if self.hidden_price else '',
                    self.url if self.url else ''])

class BaseScraper(ABC):
    locators = dict(
        product_search_result_locator = None
        )

    def __init__(self, url:str,
        page: BeautifulSoup = None,
        driver_method = 'requests',
        driver = None,
        **kwargs):
        self.url = url
        self._page = page
        self._driver = driver
        self.driver_method = driver_method
        self.kwargs = kwargs
        self._productlist = None
        logger.info(f"{driver_method} selected")
    
    @property
    def page(self):
        if self._page == None:
            if self.driver_method == 'selenium':
                self.driver.get(self.url, **self.kwargs)
                content = self.driver.page_source
                logger.info('Page loaded using Selenium')
            elif self.driver_method == 'requests':
                content = self.driver.get(self.url, **self.kwargs).content
                logger.info('Page loaded using requests')
            self._page = BeautifulSoup(content, features="lxml")
        return self._page
    
    @property
    def driver(self):
        if self._driver == None:
            if self.driver_method.lower() == 'selenium':
                self._driver = self.get_driver()
            elif self.driver_method.lower() == 'requests':
                self._driver = requests
        return self._driver
    
    def get_driver(self, need_login=False):
        driver = webdriver.Chrome()
        if need_login:
            raise NotImplementedError
        return driver
    
    def close(self):
        if self.driver_method == 'selenium':
            self.driver.close()
            logger.info('Selenium driver closed')

    def get_productlist(self):
        self._productlist_bs4 = self.page.find_all(**self.locators.get('product_search_result_locator'))
        productlist = ProductList()
        for i in self._productlist_bs4:
            try:
                productlist.append(self.parse_one_product(i))
            except:
                logger.info(f"Skipped! Parsing product {i.attrs['data-id']} failed")
        return productlist
    
    @property
    def productlist(self):
        if self._productlist == None:
            self._productlist = self.get_productlist()
        return self._productlist
    
    def parse_one_product(self, product_bs4: BeautifulSoup):
        pass