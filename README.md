# Back to the Future: Cinema is the new DeLorean

## Data Story

[Go to the website!](https://duchoud.github.io/war_and_movies/)

## Abstract
"Cinema is an edited reality and a mirror of society."
Cinema has been depicted as an edited reality and even a mirror of society, and society has endured in the past century numerous events: technological advances, wars, human rights movements etc. These historical events have influenced our society, and what we are investigating is whether these events have impacted the cinematic industry, and if yes, how.  
We will start by analyzing the speed of spread of the color cinema on black & white movies, then we will researh  the consequences of the war on genres' popularity (comedy and war) and finally explore the major cinematographic changes per genre per year in general using Natural Language Process and Time Series techniques.

## Research questions

If cinema is a mirror of society, did historical events influence cinema? If yes, how and when?

   * A: How quick did colors integrated our movies? Was this market penetration similar across genres? 
   * B: Does violence encourages people to watch violence or is laughter in cinema is acclaimed then more than ever?
   * C: Have did racism and terrorism's events impacted the integration of ethnic minority actors?

## Proposed additional datasets

 - **Dataset 1:[The Ultimate Movie Genres List](https://www.studiobinder.com/blog/movie-genres-list/)** Dataset that contains the names of the desired movie genres. An NLP can be applied to the genre of the films thanks to this dataset to come out with the desired genre names.
 - **Datasets 2:[IMDb](https://datasets.imdbws.com/)** the following two datasets from IMDb:
      - "title.ratings" contains the IMDb rating and votes information for titles of the movies.
      - "title.basics" to make the link with the dataset "title.ratings".  It gives the alphanumeric unique  identifier of the title and the titles of the movies.
 - **Dataset 3:** queries to Freebase. Dataframe with the Actor ethnicity codes(Freebase ID) and their corresponding name.
 

## Methods

### Step 1: Natural Language Processing: Metagenre Creation
- Harmonization of string format
- Extraction of subgenres from incoherent data formats
- Metagenre and subgenre table creation from the web
- Subgenre formating with stemming for similarity detection
- Robust Metagenre classification

### Step 2: Time Series: Feature Analysis
Example of features: Metagenres

- Generate dummy variables from Metagenres
- Resample our dataframe for a certain window, count the number of movies per window
- Normalize the number of views (sum per window =1)
- Aggregate using a cumulative function:
      - cummax: to see the peakyear
      - cumsum: to study the cumulative sum     
- Calculate the percent change to analyze the variation of the genres between windows
- To study the trend of a certain genre, use the trend/seasonality/residual decomposition and use the trend

### Step 3: Survey the impact of segregation-related events on the integration of ethnic minority actors.
- Queries to Freebase to get access to the dataset 3
- Feature analysis to study a trend of a certain Actor ethnicity 
- Link the trend to the corresponding segregation-related event

### Step 4: Sentiment analysis 
- Extracting feelings from plot summaries using an existing NLP model
- Use these feelings as new metadata

### Step 5: Apply feature analysis to other themes
   - Human rights (E.g Civil Rights Act de 1964 in America)
   - Political events
   - Thechnological events (E.g Popularization of the Internet, development of Netflix)
    

### Step 6: Github site building and Datastory redaction.

## Proposed timeline

- 25/11/22 Improve NLP and feature analysis / queries to Freebase 
- 02/12/22 Do all tasks related to step 3
- 09/12/22 Train the sentiment analysis
- 16/12/22 Apply analysis to the other themes
- 21/12/22 Github site building and Datastory redaction.
- 23/12/22 Milestone 3 deadline.


## Organization within the team

| Student | Task   |
|------|------|
|   Alain  | Github site building|
|     | Queries to Freebase and step 3|
|     | Develop the final text for the data story|
|   Bastien  | Apply feature analysis to other themes|
|     | Queries to Freebase and step 3|
|     | Develop the final text for the data story|
|   Nicolas  | Apply feature analysis to other themes|
|     | Improve NLP|
|     | Develop the final text for the data story|
|   Mohamed  | Github site building|
|     | Improve feature analysis|
|     | Develop a sentiment analysis|
