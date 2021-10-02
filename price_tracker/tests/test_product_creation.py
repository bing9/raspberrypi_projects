from price_tracker.src.data.create_products import *
import pytest

def test_search_class():
    p = SearchTerm('Philips Sonicare')
    assert isinstance(p.product_list, ProductList)
    assert p.parse_search_terms() == ['philips', 'sonicare']

def test_search_domain():
    with pytest.raises(SearchDomainNotImplementedError) as execinfo:
        p = SearchTerm('Dummy', 'dummy.com')