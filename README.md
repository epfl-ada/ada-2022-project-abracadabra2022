# Back to the Future: Cinema is the new DeLorean

## Abstract

The movie industry has in the late 19th and early 20th century developed massively from a very luxurious to a widespread and cheap activity to the 
point where in the 1920s it could be considered common to watch a movie. The societies have in the past century gone through a huge evolution with 
a lot of dramatic event such as wars and nuclear fear but also many technological advances, to the point that it could be argued that there has 
never been such fast changements in societies. This fast changing society and movie industry have evolved along sides through major historical 
events, theses events have obviously impacted heavily the populations, and we therefore wonder to what extent the film production and society are 
closely linked together. This is equivalent to asking if major historical events have been translated into the productions of movies. Following 
this question, we also want to observe how films with a strong link to historical event have been received by the general public. To answer this we 
will use the movie corpus dataset along with the IMDb database. Using NLP and statistic pipelines we will try to observe trends that can answer our 
questions.

## Research questions

If cinema is a mirror of society, how have historical events influenced cinema? 
A: How the advent of color cinema influenced the popularity of black & white movies? 
B: What is the impact of a war on the popularity of war films in the following years?
C: Have anti-segregation events facilitated the integration of ethnic minority actors?

## Proposed additional datasets

 - **Dataset 1:[The Ultimate Movie Genres List](https://www.studiobinder.com/blog/movie-genres-list/)** Dataset that contains the names of the desired movie genres. An NLP can be applied to the genre of the films thanks to this dataset to come out with the desired genre names.
 - **Datasets 2:[IMDb](https://datasets.imdbws.com/)** the following two datasets from IMDb:
      - "title.ratings" contains the IMDb rating and votes information for titles of the movies.
      - "title.basics" to make the link with the dataset "title.ratings".  It gives the alphanumeric unique  identifier of the title and the titles of the movies.

## Methods

### Step 1: Extract movie genre from the dataset using NLP. 

- Apply an NLP with the additional dataset 1 on the movie genres to assign the desired genre name to each film.
- After NLP, film genres must be clean.

### Step 2: Plot time series with movie genre to answer question A and B.
- Plot the number of movies of a certain genre per year. 
- Highlight the impact of an event on the popularity of a movie genre by modifying the period analyzed.
- Decompose time series to highlight a data trend.

### Step 3: Survey the impact of segregation-related events on the integration of ethnic minority actors to answer question C.
- 
-


### Step 4: Github site building and Datastory redaction.

## Proposed timeline

- 07/12/22
- 09/12/22
- 14/12/22
- 16/12/22 
- 21/12/22 Github site building and Datastory redaction.
- 23/12/22 Milestone 3 deadline.

## Organization within the team

| Student | Task   |
|------|------|
|   @bastlan3  | task1|
|     | task2|
|     | task3|
|   @duchoud  | task1|
|     | task2|
|     | task3|
|   a  | task1|
|     | task2|
|     | task3|
|   @Termote  | task1|
|     | task2|
|     | task3|
