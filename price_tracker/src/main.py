from src.data.get_searchterm_prices import main as search_price
from src.features.monitor_price_changes import main as monitor_price
from src.features.get_min_prices import calculate_min_prices
from dotenv import find_dotenv, load_dotenv
import logging
from pathlib import Path
import time

load_dotenv(find_dotenv())

log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_fmt)
logger = logging.getLogger(__name__)
# not used in this stub but often useful for finding various files
project_dir = Path(__file__).resolve().parents[1]

# find .env automagically by walking up directories until it's found, then
# load up the .env entries as environment variables
load_dotenv(find_dotenv())

counter = 0
per = 1

while True:
    try:
        search_price(project_dir)
        monitor_price(project_dir)
        if counter % (24 * 2 / per) == 0:
            # Every 2 days refresh lowest price
            logger.info(f'Refreshing lowest price...{counter}')
            calculate_min_prices(project_dir)
        logger.info('sleep 4 hours')
        time.sleep(per*60*60) # Every 4 hours
    except KeyboardInterrupt:
        break
    except:
        break
