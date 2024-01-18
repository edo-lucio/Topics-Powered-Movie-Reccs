from get_data.get_movies import update_movies
from get_data.scrape_reviews import update_reviews
from get_data.update_topics import update_topics

from insert_documents import update_movie_list, update_topics_list

YEAR_RANGE = [i for i in range(2024, 2025)] # next year ;)

## This module updates MongoDB database.
## It first queries TMDB database to retrieve MAX_MOVIES_PER_YEAR movies in the specified YEAR_RANGE
## It then gathers for the new movies their reviews from Letterboxd website 

def main():
    new_movies = update_movies(YEAR_RANGE)
    new_reviews = update_reviews(new_movies)
    new_topics = update_topics(new_movies, new_reviews)

    update_movie_list(new_movies, new_reviews)
    update_topics_list(new_topics)

if __name__ == "__main__":
    main()


    
