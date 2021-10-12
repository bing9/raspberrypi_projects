import pandas as pd
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import logging

logger = logging.getLogger(__name__)

def read_csv(path):
    try:
        df = pd.read_csv(path, sep = '\t')
        df['parse_date'] = path.name.rstrip('.tsv')
        return df
    except:
        return None

def calculate_min_prices(project_dir):
    data_dir = project_dir/'data'/'raw'
    data_external = project_dir/'data'/'external'
    with ProcessPoolExecutor() as pool:
        dfs = pool.map(read_csv, data_dir.iterdir())

    df = pd.concat(dfs)

    def clean_numeric(s, to_type = float):
        if isinstance(s, str):
            return to_type(s.strip().strip('-'))
        else:
            return s

    df['price'] = df['price'].apply(clean_numeric)

    df.sort_values(by = 'price', inplace = True)

    df.drop_duplicates(subset = ['provider', 'provider_id'], keep = 'first', inplace = True)

    df.to_csv(data_external/'lowest_price.tsv', index = False, sep = '\t')

if __name__ == '__main__':
    project_dir = Path(__file__).resolve().parents[2]
    calculate_min_prices(project_dir)