# Topics-Powered-Movie-Reccs

## Introduction 
The project collects data about movies from TMDB APIs and integrates it with reviews scraped from the Letterboxd website. 
The idea is to create a comprehensive movie database with integrated data from different sources in order to create a film reccommendation system.
Data is stored into a MongoDB server on cloud.
Executing `bot.py` launches a Telegram bot which takes user input words to reccomend movies with topics matching the input.

## Requirements
 To run this project it is first necessary to install the required dependencies through 
 `pip install -r requirements.txt `
 It is also necessary to have a W2V model inside the project folder (e.g. GoogleNews-vectors-negative300.bin)

## Main Modules
`update_db.py` module updates the database with both movie data collected from public APIs and scraped review.
`scoring.py` module computes scores for each movie based upon user's inputs words



