import requests
from bs4 import BeautifulSoup
from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

class ProductList(list):
    def save_prices_to_db(self, path: Path):
        file_name = datetime.now().strftime("%Y-%m-%d %I:%M%p")
        to_save_data = [p.to_records() for p in self]
        if to_save_data:
            with open(path/f"{file_name}.tsv", 'w') as file:
                file.writelines(to_save_data)
        

@dataclass
class Product:
    provider: str
    provider_id: str
    name: str
    url: str
    price: str
    original_price: str

    def to_records(self):
        return '\t'.join([self.provider if self.provider else '', 
                    self.provider_id if self.provider_id else '', 
                    self.name  if self.name else '', 
                    self.price  if self.price else '', 
                    self.original_price  if self.original_price else '' ])

class BaseScraper(ABC):
    def __init__(self, url:str,
        page: BeautifulSoup = None,
        **kwargs):
        self.url = url
        self._page = page
        self.kwargs = kwargs
    
    @property
    def page(self):
        if self._page == None:
            content = requests.get(self.url, **self.kwargs).content
            self._page = BeautifulSoup(content, features="lxml")
        return self._page