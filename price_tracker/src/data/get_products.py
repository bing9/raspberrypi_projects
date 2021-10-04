from typing import Iterable, Union
import time
from base import ProductList
from scrape_bol import BolScraper

class SearchTerm:
    '''Search term is the product name for searching'''
    implemented_search_domains = ['bol.com']

    def __init__(self, search_term: str = None, 
        search_domain: str = 'bol.com',
        search_urls: list = None,
        productlist: ProductList = None,
        max_pages: int = 5):
        self.search_term = search_term
        self._productlist = productlist
        self.search_domain = search_domain
        self._search_urls = [search_urls] if isinstance(search_urls, str) else search_urls
        self.max_pages = max_pages
        if self.search_domain not in SearchTerm.implemented_search_domains:
            raise SearchDomainNotImplementedError(
                f"Please Use one of the implemented Domains: {SearchTerm.implemented_search_domains}")

    @property
    def productlist(self):
        if self._productlist == None:
            self._productlist = self.get_productlist()
        return self._productlist

    @property
    def search_urls(self):
        if self._search_urls == None:
            self._search_urls = self.construct_search_urls()
        return self._search_urls

    def get_productlist(self):
        pl = ProductList()
        for i in self.search_urls:
            try:
                page_pl = self.Scraper(i).get_productlist()
                if page_pl == []:
                    break
                if isinstance(page_pl, list):
                    pl.extend(page_pl)
                else:
                    pl.append(page_pl)
                time.sleep(5)
            except: 
                break
        return pl
    
    @property
    def Scraper(self):
        if 'bol' in self.search_domain:
            return BolScraper
        else:
            raise NotImplementedError

    def parse_search_terms(self):
        return [i.lower() for i in self.search_term.strip().split(' ')]

    def construct_search_urls(self):
        search_text = '+'.join(self.parse_search_terms())
        if 'bol' in self.search_domain:
            # https://www.bol.com/nl/nl/s/?page=2&searchtext=philips+sonicare&view=list
            return [f'https://www.bol.com/nl/nl/s/?page={i}&searchtext={search_text}&view=list' for i in range(1, self.max_pages+1)]
        else:
            NotImplementedError

class SearchDomainNotImplementedError(Exception):
    pass