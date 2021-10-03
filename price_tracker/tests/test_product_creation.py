from price_tracker.src.data.create_products import *
import pytest

def test_search_class():
    p = SearchTerm('Philips Sonicare')
    assert isinstance(p.productlist, ProductList)
    assert p.parse_search_terms() == ['philips', 'sonicare']

def test_search_domain():
    with pytest.raises(SearchDomainNotImplementedError) as execinfo:
        SearchTerm('Dummy', 'dummy.com')

def test_search_urls():
    p = SearchTerm(search_urls = 'test_url')
    assert p._search_urls == ['test_url']

@pytest.mark.webtest
def test_search_terms():
    s = SearchTerm(search_term='philips sonicare', search_domain = 'bol.com')
    assert len(s.productlist) >=100 and len(s.productlist) <=200