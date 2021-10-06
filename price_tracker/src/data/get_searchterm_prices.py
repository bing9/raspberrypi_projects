# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from src.data.get_products import SearchTerm
from src.data.base import ProductList
import os
import time

# @click.command()
# @click.argument('input_filepath', type=click.Path(exists=True))
# @click.argument('output_filepath', type=click.Path())
# input_filepath, output_filepath
def main(project_dir):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')
    productlist = ProductList()
    for search_term in eval(os.environ['bol_search_terms']):
        s = SearchTerm(search_term=search_term, search_domain = 'bol.com',
            max_pages = 1, driver_method = 'selenium')
        pl = s.productlist
        productlist.extend(pl)
        time.sleep(5)
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