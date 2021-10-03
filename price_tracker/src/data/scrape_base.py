import requests
from bs4 import BeautifulSoup
from abc import ABC

class BaseScraper(ABC):
    def __init__(self, url:str,
        **kwargs):
        self.url = url
        self.kwargs = kwargs

    def get_webcontent(self):
        soup = BeautifulSoup(requests.get(self.url, **self.kwargs))
        return soup