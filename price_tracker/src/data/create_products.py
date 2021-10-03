from typing import Union
from dataclasses import dataclass
from datetime import datetime

class ProductList(list):
    pass

@dataclass
class Product:
    provider: str
    provider_id: str
    name: str
    url: str
    price: str
    original_price: str
    scrape_datetime: datetime


class SearchTerm:
    '''Search term is the product name for searching'''
    implemented_search_domains = ['bol.com']

    def __init__(self, search_term: str, 
        search_domain: str = 'bol.com',
        product_list: ProductList = None):
        self.search_term = search_term
        self._product_list = product_list
        self.search_domain = search_domain
        if self.search_domain not in SearchTerm.implemented_search_domains:
            raise SearchDomainNotImplementedError(
                f"Please Use one of the implemented Domains: {SearchTerm.implemented_search_domains}")

    @property
    def product_list(self):
        if self._product_list == None:
            self._product_list = self.get_product_list()
        return self._product_list

    def get_product_list(self):
        return ProductList()

    def parse_search_terms(self):
        return [i.lower() for i in self.search_term.strip().split(' ')]

    def construct_search_url(self):
        pass

class SearchDomainNotImplementedError(Exception):
    pass