from movies.models import Movie, Rating

import numpy as np 
import pandas as pd

movies = pd.DataFrame(list(Movie.objects.values_list('id','title')))
ratings  = pd.DataFrame(list(Rating.objects.values_list('user_id','movie_ids','rating')))
#print(movies)
#ratings[0]=pd.to_numeric(ratings[0])
#ratings[1]=pd.to_numeric(ratings[1])
#ratings[2]=pd.to_numeric(ratings[2])
#movies[0]=pd.to_numeric(movies[0])

movies.columns=["movie_id","title"]
ratings.columns=['userId', 'movie_id', 'rating']

ratings2 = ratings.copy()


ratings = pd.merge(movies,ratings)

userRatings = ratings.pivot_table(index=['userId'],columns=['title'],values='rating')
userRatings.head()

corrMatrix = userRatings.corr(method='pearson')
corrMatrix.head(100)


def get_similar(movie_name,rating):
    similar_ratings = corrMatrix[movie_name]*(rating-2.5)
    similar_ratings = similar_ratings.sort_values(ascending=False)
    #print(type(similar_ratings))
    return similar_ratings

def func(uid):
    global ratings2
    user_rat=ratings2.loc[ratings2['userId'] == uid]
    user_prof=[]
    for _, row in user_rat.iterrows():
        user_prof.append((row["movie_id"],row["rating"]))
    similar_movies = pd.DataFrame()
    for movie,rating in user_prof:
        similar_movies = similar_movies.append(get_similar(movie,rating),ignore_index = True)

    print(similar_movies.sum().sort_values(ascending=False).head(20))





func(1)