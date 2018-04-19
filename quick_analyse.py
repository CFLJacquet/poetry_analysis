import pandas
import json
from poetry_analysis.utils.text import tokenize, get_tfidf, get_count, load_json, get_json_dataframe

poems = load_json('./data/poems_extracted.json')
df_poems = get_json_dataframe(poems)

# 58 different authors. Victor Hugo is the most represented author (148 texts)
print(df_poems['author'].describe())

# 189 different books. First : Les fleurs du mal (freq=39)
print(df_poems['book'].describe())

# 136 different themes. First : l'amour (54 poems)
print(df_poems['theme'].describe())