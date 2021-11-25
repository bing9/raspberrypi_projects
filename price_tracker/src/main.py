from src.data.get_searchterm_prices import main as search_price
from src.features.monitor_price_changes import main as monitor_price
from src.features.get_min_prices import calculate_min_prices
from dotenv import find_dotenv, load_dotenv
import logging
from pathlib import Path
import time

log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_fmt)
logger = logging.getLogger(__name__)
# not used in this stub but often useful for finding various files
project_dir = Path(__file__).resolve().parents[1]


counter = 0
per = 1

while True:
    try:
        # find .env automagically by walking up directories until it's found, then
        # load up the .env entries as environment variables
        load_dotenv(find_dotenv(), override=True)
        search_price(project_dir)
        monitor_price(project_dir)
        logger.info('Refreshing lowest price...')
        calculate_min_prices(project_dir, method = 'quick')
        logger.info(f'Iteration {counter} completed. Sleep {per} hours')
        time.sleep(per*60*60) # Every 4 hours
    except KeyboardInterrupt:
        break
    except:
        break
