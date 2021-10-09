# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from src.data.searchterm import SearchTerm
from src.data.base import ProductList
import os
import time
from concurrent.futures import ProcessPoolExecutor

def execute_search(from_env):
    search_term, search_domain = from_env
    if 'bol' in search_domain\
        or 'bcc' in search_domain:
        driver_method = 'requests'
    else:
        driver_method = 'selenium'
    s = SearchTerm(search_term=search_term, search_domain = search_domain,
                max_pages = 1, driver_method = driver_method)
    return s.productlist
            

# @click.command()
# @click.argument('input_filepath', type=click.Path(exists=True))
# @click.argument('output_filepath', type=click.Path())
# input_filepath, output_filepath
def main(project_dir, max_worker = 1):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')
    productlist = ProductList()
    env_search_terms = [i for i in os.environ if 'search_terms' in i]

    iterator = []
    for env_search_term in env_search_terms:
        search_domain = env_search_term.split('_')[0]
        for search_term in eval(os.environ[env_search_term]):
            iterator.append((search_term, search_domain))
    if max_worker >1:
        with ProcessPoolExecutor(max_workers=3) as pool:
            result = pool.map(execute_search, iterator)
            
        for pl in result:     
            productlist.extend(pl)
    else:
        for i in iterator:
            pl = execute_search(i)
            productlist.extend(pl)
            time.sleep(2)

    productlist.save_prices_to_db(path = project_dir/'data'/'raw')
    return 'success'

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
