import numpy as np
import pandas as pd
import json


with open('redditgetsdrawn.txt', 'r') as f:
    txt = f.read()

lines = txt.split('\n')
rows = [json.loads(line) for line in lines if line <> '']
cache = dict([(row['id'], row) for row in rows if 'id' in row])
df = pd.DataFrame(cache.values())
df['parent'] = df[df.body.notnull()]['permalink'].str.replace(r'.*/comments/([^/]*)/.*', r'\1')

