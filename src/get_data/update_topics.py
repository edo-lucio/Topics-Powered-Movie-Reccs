from gensim import corpora
from gensim.models import LdaModel

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import sys
sys.path.append('')

from src.helpers import read_files, x

import os
import csv

import re

import pandas as pd
from configurations.config import DATA_PATH

import string 

## Perform topic modeling of the text associated with each movie

NUM_TOPICS = 2

def pre_process(texts, custom_stopwords=None):
    preprocessed_texts = []

    for text in texts:
        text = text.lower() 

        text = re.sub(r'\d+', '', text)

        text = text.translate(str.maketrans('', '', string.punctuation))

        text = text.strip()

        words = word_tokenize(text)

        stop_words = set(stopwords.words('english'))

        if custom_stopwords:
            stop_words.update(custom_stopwords)

        words = [word for word in words if word.lower() not in stop_words]

        preprocessed_texts.append(words)

    return preprocessed_texts

def create_dictionary(tokenized_docs):
    return corpora.Dictionary(tokenized_docs)

def create_dtm(dictionary, tokenized_docs):
    return [dictionary.doc2bow(doc) for doc in tokenized_docs]

def topic_model(document):
    token_documents = pre_process(document, ["aki", "i", "it", "movie", "one", "film", "the", "would", "ok", "like", "getting",
                                        "more", "ki", "also", "made", "yet", "know", "get", "telling", "null", "movie", "film", 
                                        "director", "watch", "watching", "even", "mr"])
    
    dictionary = create_dictionary(token_documents)
    dtm = create_dtm(dictionary, token_documents)

    lda_model = LdaModel(dtm, num_topics=NUM_TOPICS, id2word=dictionary, passes=15)
    topics_dict = { i: lda_model.show_topic(i) for i in range(NUM_TOPICS) }

    return topics_dict

def update_topics(movies, reviews):
    text = x(movies, reviews)
    text = text[["id", "text"]]
    text = text.groupby("id")

    topics = pd.DataFrame()
    path = "./data/topics.csv"
    
    for id, group in text:
        pp = group["text"].to_list()
        topics = topic_model(pp)

        write_header = not os.path.isfile(path) or os.stat(path).st_size == 0

        with open(path, 'a', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)

            if write_header:
                csv_writer.writerow(['id', 'word', 'weight'])
            
            for _, topic in topics.items():
                for word, weight in topic:
                    csv_writer.writerow([id, word, weight])

if __name__ == "__main__":
    data_frames = read_files(DATA_PATH)

    movies = data_frames["movies"]
    reviews = data_frames["reviews"]

    update_topics(movies, reviews)















