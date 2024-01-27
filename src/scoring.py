from gensim.models import KeyedVectors

from sklearn.neighbors import NearestNeighbors

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

from pymongo.mongo_client import MongoClient
import os
import certifi

import pandas as pd
import numpy as np

import ast

from string import punctuation

## Scores movies based on the user input and returns them

model_path = 'GoogleNews-vectors-negative300.bin'
word2vec_model = KeyedVectors.load_word2vec_format(model_path, binary=True, limit=100000)

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return 'a'  # adjective
    elif treebank_tag.startswith('V'):
        return 'v'  # verb
    elif treebank_tag.startswith('N'):
        return 'n'  # noun
    elif treebank_tag.startswith('R'):
        return 'r'  # adverb
    else:
        return 'n'  # default to noun

def preprocess_text(text):
    tokens = word_tokenize(text.lower())

    stop_words = set(stopwords.words('english') + list(punctuation))
    tokens = [token for token in tokens if token not in stop_words]

    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token, pos=get_wordnet_pos(tag))
              for token, tag in pos_tag(tokens)]
    
    return tokens

def get_nearest_words(input_words):
    input_words = [preprocess_text(word) for word in input_words]
    input_words = list(np.concatenate(input_words))
    k_neighbors = 4

    input_vectors = [word2vec_model[word] for word in input_words if word in word2vec_model.index_to_key]

    knn_model = NearestNeighbors(n_neighbors=k_neighbors, metric='cosine')
    knn_model.fit(word2vec_model.vectors)

    try: 
        distances, indices = knn_model.kneighbors(input_vectors)
        nearest_words = []
    except: 
        raise(Exception("error"))

    for i, input_word in enumerate(input_words):
        for j, idx in enumerate(indices[i]):
            neighbor_word = word2vec_model.index_to_key[idx]
            nearest_words.append(neighbor_word)

    
    print(nearest_words)

    return nearest_words

class Score:
    def __init__(self, movies, topics) -> None:
        self.movies = movies
        self.topics = topics

    def score(self, input_words):
        words_vector = get_nearest_words(input_words)
        movie_scores = []

        for _, _, _, id, topics_list in self.topics.itertuples():
            movie_score = {}
            topics_list = ast.literal_eval(topics_list)
            intersection = set([x["word"] for x in topics_list]).intersection(set(words_vector))
            score = sum([x["weight"] for x in topics_list if x ["word"] in intersection])

            movie_score["id"] = id
            movie_score["score"] = score
            movie_scores.append(movie_score)

        movie_scores = pd.DataFrame(movie_scores)
        return movie_scores.sort_values(by="score", ascending=False)

    def top_k_similiar_movies(self, input_words, k):
        scores = self.score(input_words)

        movies = pd.merge(scores, self.movies, how="inner", on="id")
        movies = movies.sort_values(by="score", ascending=False)
        movies = movies[["score", "title", "year"]].drop_duplicates()
        reccomendations = []

        for index, weight, movie, year in movies[["score", "title", "year"]].itertuples():
            if index <= k+12 and weight > 0:
                reccomendations.append(f'{ movie } ({ year }) - { round(weight * 100, 2) }')
        
        return reccomendations

if __name__ == "__main__":

    movies = pd.read_csv("./data/movies_collection.csv")
    topics = pd.read_csv("./data/topics_collection.csv")

    score = Score(movies, topics)
    score.top_k_similiar_movies(["depressed", "mothers"], 12)













