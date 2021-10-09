import time
from src.data.scrape_mediamarkt import MediaMarktScraper
from src.data.scrape_bcc import BCCScraper
from src.data.base import ProductList
from src.data.scrape_bol import BolScraper
import logging

logger = logging.getLogger(__name__)

class SearchTerm:
    '''Search term is the product name for searching'''
    implemented_search_domains = ['bol.com', 'mediamarkt.nl', 'bcc.nl']

    def __init__(self, search_term: str = None, 
        search_domain: str = 'bol.com',
        search_urls: list = None,
        productlist: ProductList = None,
        max_pages: int = 5,
        **kwargs
        ):
        self.search_term = search_term
        self._productlist = productlist
        self.search_domain = search_domain
        self._search_urls = [search_urls] if isinstance(search_urls, str) else search_urls
        self.max_pages = max_pages
        self.kwargs = kwargs
        if self.search_domain in SearchTerm.implemented_search_domains\
            or self.search_domain in [i.split('.')[0] for i in SearchTerm.implemented_search_domains]:
            pass
        else:
            raise SearchDomainNotImplementedError(
                f"Entered {self.search_domain}. Please Use one of the implemented Domains: {SearchTerm.implemented_search_domains}")

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
                self.scraper = self.Scraper(i, driver_method = self.kwargs.get('driver_method', 'requests'))
                page_pl = self.scraper.productlist
                if page_pl == []:
                    break
                if isinstance(page_pl, list):
                    pl.extend(page_pl)
                else:
                    pl.append(page_pl)
                self.scraper.close()
                time.sleep(5)
            except:
                self.scraper.close()
                break
        return pl
    
    @property
    def Scraper(self):
        if 'bol' in self.search_domain:
            return BolScraper
        elif 'mediamarkt' in self.search_domain:
            return MediaMarktScraper
        elif 'bcc' in self.search_domain:
            return BCCScraper
        else:
            raise NotImplementedError

    def parse_search_terms(self):
        logger.info(f"preparing search {self.search_term} in domain {self.search_domain}")
        return [i.lower() for i in self.search_term.strip().split(' ')]

    def construct_search_urls(self):
        search_text = '+'.join(self.parse_search_terms())
        if 'bol' in self.search_domain:
            # https://www.bol.com/nl/nl/s/?page=2&searchtext=philips+sonicare&view=list
            return [f'https://www.bol.com/nl/nl/s/?page={i}&searchtext={search_text}&view=list' for i in range(1, self.max_pages+1)]
        elif 'mediamarkt' in self.search_domain:
            # https://www.mediamarkt.nl/nl/search.html?query=galaxy+tab+s7&searchProfile=onlineshop&channel=mmnlnl&page=2
            return [f'https://www.mediamarkt.nl/nl/search.html?query={search_text}&searchProfile=onlineshop&channel=mmnlnl&page={i}' for i in range(1, self.max_pages+1)]
        elif 'bcc' in self.search_domain:
            # https://www.bcc.nl/search?fh_location=%2F%2Fcatalog01%2Fnl_NL%2Fchannel%3E%7Bm2ebcc2enl%7D&search=philips%2Bsonicare
            return [f'https://www.bcc.nl/search?search={search_text}&index={i*18}' for i in range(0, self.max_pages)]
        else:
            NotImplementedError

class SearchDomainNotImplementedError(Exception):
    pass