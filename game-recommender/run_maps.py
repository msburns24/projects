from pathlib import Path
import re
import pandas as pd
import numpy as np
from fuzzywuzzy import process

from tqdm import tqdm
tqdm.pandas()


# Setup paths
data_dir = Path(__file__).parent / 'data'
assert data_dir.exists(), f"Unable to locate directory: '{data_dir}'"
steam_200k_path = data_dir / 'steam-200k.csv'
games_path = data_dir / 'games.csv'


# Load Datasets
steam_200k_cols = ['user_id', 'game_title', 'behavior_name', 'hours', 'extra']
steam_200k = pd.read_csv(steam_200k_path, names=steam_200k_cols)
games_raw = pd.read_csv(games_path, escapechar='\\')


# Initial Cleaning
games = games_raw[['app_id', 'name']].rename(columns={'name': 'game_title'})
playtime = (
    steam_200k
    .query(f"behavior_name == 'play'")
    .groupby(['user_id', 'game_title'], as_index=False)
    [['hours']].sum()
)


def normalize_title(title: str) -> str:
    title = title.lower()
    title = title.strip()
    title = re.sub(r'[^\w\s]', '', title)
    title = re.sub(r'\s+', '', title)
    return title

playtime_norm = playtime.copy()
games_norm = games.copy()
playtime_norm['game_title'] = playtime_norm['game_title'].map(normalize_title)
games_norm['game_title'] = games['game_title'].map(normalize_title)
df = playtime_norm.merge(games_norm, how='left')


# Apply fuzzy matching
def get_best_match(title: str, choices: list[str], threshold: int=90):
    best_match, score = process.extractOne(title, choices)
    return (best_match, score) if score >= threshold else (None, score)

unmatched = df[df['app_id'].isnull()].copy()
name_to_app_id = dict(zip(games_norm['game_title'], games_norm['app_id']))
all_game_names = list(name_to_app_id.keys())
new_cols = ['fuzzy_match', 'fuzzy_score']
unmatched[new_cols] = unmatched['game_title'].progress_apply(
    lambda x: pd.Series(get_best_match(x, all_game_names, threshold=90))
)
unmatched['fuzzy_app_id'] = unmatched['fuzzy_match'].map(name_to_app_id)
df.update(unmatched[['fuzzy_app_id']])
df['app_id'] = df['app_id'].fillna(df['fuzzy_app_id'])


# Final match coverage after fuzzy matching
final_match_coverage = df['app_id'].notnull().mean()
print(f'Final Match coverage: {final_match_coverage:.2%}')

df.to_csv('data/matched.csv', index=False)
print('Wrote data to file.')