import sys
from pathlib import Path
project_dir = Path(__file__).resolve().parents[2]
helper_folder = str(project_dir.parent / 'Utils')
sys.path.insert(0, helper_folder)
# print(helper_folder)
import notifications as n
from dotenv import find_dotenv, load_dotenv
import os
import pandas as pd

# find .env automagically by walking up directories until it's found, then
# load up the .env entries as environment variables
load_dotenv(find_dotenv())
data_dir = project_dir/'data'/'external'
max_file = data_dir /'new_price.tsv'
second_max_file = data_dir / 'old_price.tsv'

df_max = pd.read_csv(max_file, sep = '\t')

df_second_max = pd.read_csv(second_max_file, sep = '\t')

df = df_second_max.compare(df_max)

df = pd.merge(df_second_max, df_max, left_on = ['provider_id'], right_on = ['provider_id'], 
        suffixes = (None, '_old'))

df['discount'] = 1 - df['price'] / df['price_old']

df_notify = df[df['discount'] >=0.1]

cols = ['provider', 'name', 'price', 'price_old', 'URL']

if len(df_notify)>0:
    records = df_notify.to_dict(orient = 'records')
    r = []
    for record in records:
        price = record['price']
        original_price = record['price_old']
        url = record['URL']
        r.append('\n'.join([record['provider'], record['name'], f'{price}  ~{original_price}~',
            f'<{url}|Product Link>'
            ])
                                                                                               )
    message = '😍 Price decreased! \n'+ '\n\n'.join(r)
    n.send_hangout(message, os.environ['webhook'],
            os.environ['space_id'], os.environ['thread_id'])
else:
    # message = "😫 No price changes!"
    pass

