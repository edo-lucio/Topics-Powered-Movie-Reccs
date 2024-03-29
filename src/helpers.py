import re
import os
import pandas as pd
import nltk

from multiprocessing import Pool

import sys
sys.path.append('')

from configurations.config import MOVIES_PATH, REVIEWS_PATH

def remove_substring_between_chars(input_string, start_char, end_char):
    pattern = re.escape(start_char) + '.*?' + re.escape(end_char)
    result = re.sub(pattern, '', input_string)
    return result
 
def wrangle_columns(df):
    df["year"] = pd.to_datetime(df["release_date"], format='%Y-%m-%d').dt.year
    df = df.reset_index(drop=True)

    return df

def convert_star_ratings(rating):
    stars_count = len([i for i in rating if i == "★"])
    half_star = len([i for i in rating if i == "½"])/2

    return stars_count + half_star or None

def process_review(text):
    text = remove_substring_between_chars(text, "<", ">")
    text = text.rstrip()
    pattern = re.compile('[^a-zA-Z0-9 ]+')
    text = re.sub(pattern, " ", text)

    return text

def read_files(path):
    dir = os.listdir(path)
    data_frames = {}

    for file in dir:
        df = pd.read_csv(f'{path}/{file}')
        data_frames[file.split(".")[0]] = df

    return data_frames

def download_updates():
    nltk.download('wordnet')

def x(movies, reviews):
    movies = movies[["id", "title", "original_title", "overview", "year"]]
    movies = movies.drop_duplicates()
    reviews = reviews[["id", "review"]]
    
    text = pd.merge(movies, reviews, on='id', how='inner')
    text["overview"] = text["overview"].drop_duplicates()
    text['overview'] = text['overview'].fillna('')
    text['review'] = text['review'].fillna('')
    text["text"] = text["overview"] + text["review"]

    # text = pd.DataFrame(text.groupby('id')['text'].apply(lambda group: ' '.join(map(str, group.values.flatten()))).reset_index())
    return text

def get_text():
    movies = pd.read_csv(MOVIES_PATH)
    reviews = pd.read_csv(REVIEWS_PATH)
    text = x(movies, reviews)

    return text["text"].to_list()

def write_to_csv(df, path):
    file_exists = os.path.isfile(path)

    if not file_exists or os.stat(path).st_size == 0:
        df.to_csv(path, mode="w", index=False) 
    else:
        df.to_csv(path, mode="a", index=False, header=False)
