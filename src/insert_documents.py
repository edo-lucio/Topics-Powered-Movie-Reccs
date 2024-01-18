from helpers import read_files
import sys
sys.path.append('')

from configurations.config import DATA_PATH

from pymongo.mongo_client import MongoClient
import certifi

from dotenv import load_dotenv
load_dotenv()

import os
import logging

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

## This module integrates movies and reviews data and pushes the documents into a DB

ACC_DB = os.getenv("DB_ACC")

client = MongoClient(ACC_DB, ssl_ca_certs=certifi.where())
db = client.get_database("movies_db")
movies_collection = db.get_collection("movies_list")
topics_collection = db.get_collection("topics_list")

def create_movie_document(movies, id):
   movie = movies[movies["id"] == id].to_dict(orient='records')
   movie_document = {key: list(set([d[key] for d in movie]))[0] if len(set([d[key] for d in movie])) == 1 else list(set([d[key] for d in movie])) for key in movie[0]}

   return movie_document

def create_review_document(reviews, id):
   reviews_document = reviews[reviews["id"] == id][["review", "reviewer", "rating"]].to_dict(orient='records')
   return reviews_document

def create_topic_document(topics, id):
   topics_document = topics[topics["id"] == id][["word", "weight"]].to_dict(orient='records') 
   topics_document = { "id": id, "topics": topics_document }
   return topics_document

def insert_to_movies_list(movies, reviews):
   ids = min([movies["id"].unique(), reviews["id"].unique()], key=len)
   documents = []

   for movie_id in ids:
      movie_document  = create_movie_document(movies, movie_id)
      movie_reviews = create_review_document(reviews, movie_id)
      movie_document["reviews"] = movie_reviews

      documents.append(movie_document)

   movies_collection.insert_many(documents)

def insert_to_topic_list(topics):
   ids = topics["id"].unique()
   topics_docs = []

   for movie_id in ids:
      topics_doc = create_topic_document(topics, movie_id)

      if bool(topics_doc) == False:
         continue
      
      topics_doc["id"] = topics_doc["id"].item()
      topics_docs.append(topics_doc)
   
   topics_collection.insert_many(topics_docs)

def update_db():
   data = read_files(DATA_PATH)
   movies = data["movies"]
   reviews = data["reviews"]
   topics = data["topics"]

   insert_to_movies_list(movies, reviews)
   # insert_to_topic_list(topics)

   movies_collection = db.get_collection("movies_list")
   # topics_collection = db.get_collection("topics_list")

   pd.DataFrame(list(movies_collection.find())).to_csv("./data/movies_collection.csv")
   # pd.DataFrame(list(topics_collection.find())).to_csv("./data/topics_collection.csv")

if __name__ == "__main__":
   update_db()



































