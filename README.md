# From Frontline to Frontrow

## Data Story

[Go to the website!](https://duchoud.github.io/adawebsite/)

## Abstract

"Cinema is an edited reality and a mirror of society."
Cinema has been depicted as an edited reality and even a mirror of society, and society has endured in the past century numerous events: technological advances, wars, human rights movements etc. These historical events have influenced our society, and what we are investigating is whether these events have impacted the cinematic industry, and if yes, how. Our analysis focuses uniquely on wars and their impact on films. 
We will start by introducing the few wars we will be looking at. Then we will see if these wars have a cultural impact. Finally we will see if we can get a winner from these bloody events. 

## Research questions

If cinema is a mirror of society, did wars influence cinema? If yes, how and when?

   * A:  Does war have a cultural impact and more specifically on movies?
   * B:  There are no winners in wars. Is it true in movies?
   * C:  Wars affect the peception that we have to certain movies, but does it also affect our perception of movie genres itself? 
   
## Proposed additional datasets

 - **Dataset 1:[The Ultimate Movie Genres List](https://www.studiobinder.com/blog/movie-genres-list/)** Dataset that contains the names of the desired movie genres. An NLP can be applied to the genre of the films thanks to this dataset to come out with the desired genre names.
 - **Datasets 2:[IMDb](https://datasets.imdbws.com/)** the following two datasets from IMDb:
      - "title.ratings" contains the IMDb rating and votes information for titles of the movies.
      - "title.basics" to make the link with the dataset "title.ratings".  It gives the alphanumeric unique  identifier of the title and the titles of the movies.
 - **Dataset 3:** queries to Freebase. Dataframe with the Actor ethnicity codes(Freebase ID) and their corresponding name.
 
## Methods

#### External libraries

##### Built in librairy
tqdm

##### Pip libraires
numpy, json, pandas

##### Visualization librairies
plotly.express, matplotlib.pyplot, seaborn

##### Natural Language Processing librairies
nltk, re

##### Calculating libraries
scipy, random

##### Statistical librairies
pingouin 

##### Import libraries
requests, bs4, pickle

##### Date libraries
datetime, time

##### Cartography libraries
geopandas, geopy, requests

##### Other libraries
csv, dateutil.relativedelta, utils.genres, pandas_profiling

### Data preparation:
during data exploration we realised that there was many genre that were extremely similar or 2 genre joined together. To tackle this problem we used stemming to find similar genres, and then applied functions to clean the genre and separate the ones that needed to be. This process allowed us to end up with 24 genres that we exploded into dummy variables.

### Heatmaps:
The heatmaps are generated using the metadata's genres, and the sentiment analysis of the movie plots using the VADER library that outputs among other things a score between -1 and 1 per movie plot to show it's negativity or positivity. Once these two datasets are joined using the movie ids we resample the data per release year and show the average sentiment per genre per year.

### Wordclouds
The wordclouds are generated using the movie plot  and metadata datasets to be able to have per-genre wordclouds. To achieve wordcloud we clean the data and tokenize it, we also perform a sentiment analysis using TextBlob to have wordclouds of only positive or negative words. Having some data in the right format we then select the time interval wished, and then use the WordCloud library to find the most important words and create the wordcloud. We also added a list of words that did not interest us which mainly consist of names or number.

### Feature extraction
Use queries to wikidata to extract the genres corresponding to the freebase id and build a new dataset


## Organization within the team

| Student | Task   |
|------|------|
|   Alain  | Web site|
|     |  Data story|
|     |ReadMe|
|   Bastien  | Heatmap|
|     | Wordcloud|
|   Nicolas  | Interactive map|
|     | Violin plot|
|   Mohamed  | War map|
|     | NLP|

