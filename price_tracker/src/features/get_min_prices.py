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

def calculate_min_prices(project_dir, method = 'quick'):
    data_dir = project_dir/'data'/'raw'
    data_external = project_dir/'data'/'external'
    data_new = data_external / 'new_price.tsv'
    if method == 'quick':
        loop_dir = data_external
    else:
        loop_dir = data_dir
    with ProcessPoolExecutor() as pool:
        dfs = pool.map(read_csv, loop_dir.iterdir())

    df = pd.concat(dfs)

    def clean_numeric(s, to_type = float):
        if isinstance(s, str):
            s = s.strip().strip('-')
            if '.' in s:
                return to_type(s.replace(',', ''))
            elif ',' in s:
                return to_type(s.replace(',', '.'))
            else:
                return to_type(s)
        else:
            return s

    for i in ['price', 'original_price', 'hidden_price']:
        df[i] = df[i].apply(clean_numeric)

    df_max = df.copy()
    df_max.sort_values(by = 'price', ascending = False, inplace = True)
    df_max.drop_duplicates(subset = ['provider', 'provider_id'], inplace = True)

    df_min = df.groupby(['provider', 'provider_id']).agg(name = ('name', 'max'), 
            price = ('price', 'min'), max_price = ('price', 'max'),
            original_price = ('original_price', 'max'), 
            hidden_price = ('hidden_price', 'max'),
            parse_date = ('parse_date', 'max'),
            ).reset_index()

    df_new = read_csv(data_new)
    df_new = df_new[['provider', 'provider_id', 'price', 'parse_date', 'URL']]
    df_new.rename(columns = {'price': 'current_price', 
            'parse_date':'current_parse_date'},
            inplace = True)

    df_min = pd.merge(df_min, df_new, on = ['provider', 'provider_id'], how = 'left')
    df_min.sort_values(by = 'price', inplace = True)
    
    df_min.to_csv(data_external/'lowest_price.tsv', index = False, sep = '\t')
    df_max.to_csv(data_external/'highest_price.tsv', index = False, sep = '\t')

if __name__ == '__main__':
    project_dir = Path(__file__).resolve().parents[2]
    calculate_min_prices(project_dir, method = 'quick')
