import requests
from bs4 import BeautifulSoup
from abc import ABC

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