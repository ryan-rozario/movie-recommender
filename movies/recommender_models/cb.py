import numpy as np
from sklearn.neighbors import NearestNeighbors

from evaluator import Evaluator
from dataset_handler import DatasetHandler

datasetmllatest = "ml-latest-small"
dataset1M = "ml-1m"

dataset_handler = DatasetHandler(datasetmllatest)
user_ratings = dataset_handler.load_users_ratings()

class ContentBasedRecommender(object):
    def __init__(self, dataset_handler):
        self.dataset_handler = dataset_handler
        self.movies_vectors = self.dataset_handler.load_movies()
    
    def train(self, train_set):
        pass
    
    def top(self, user_profile, topN):	
        return self._cosineKNN_all_movies(user_profile[0], topN)
    
    def predict_rating(self, user_profile, movieId):
        nearest_watched_movies = self._cosineKNN_movies_subset(user_profile[1].keys(), movieId, 5)
        return np.average(np.array([user_profile[1][movie] for movie in nearest_watched_movies]))
        
    def create_user_profile(self, user_ratings):
        return (
            np.average(
                np.array([
                    self.movies_vectors[self.dataset_handler.id2index(movie)]
                    for (movie, rating) in user_ratings.items()
                ]),
                weights=np.array(list(user_ratings.values())),
                axis=0
            ),
            user_ratings
        )
    
    def present_user_profile(self, user_profile):
        print("User favourite genre:", self.dataset_handler.feature_index2genre(np.argmax(user_profile[0])))
        print("User ratings:")
        for (movieId, rating) in user_profile[1].items():
            movie_vector = self.movies_vectors[self.dataset_handler.id2index(movieId)]
            print("{} {}: {}".format(
                self.dataset_handler.id_to_title[movieId],
                self.dataset_handler.movie_vector2genres(movie_vector),
                rating
            ))
    
    def present_recommendations(self, recommendations):
        print("Recommended movies:")
        for movieId in recommendations:
            movie_vector = self.movies_vectors[self.dataset_handler.id2index(movieId)]
            print("{} {}".format(
                self.dataset_handler.id_to_title[movieId],
                self.dataset_handler.movie_vector2genres(movie_vector)
            ))
    
    def _cosineKNN_all_movies(self, user_profile, k):
        nbrs = NearestNeighbors(metric='cosine', algorithm='brute')
        nbrs.fit(self.movies_vectors)
        return self.dataset_handler.indices2ids(nbrs.kneighbors(np.array([user_profile]), k, return_distance=False)[0])
    
    def _cosineKNN_movies_subset(self, movies_subset, movieId, k):
        nbrs = NearestNeighbors(k, metric='cosine', algorithm='brute')
        movies_with_ids = np.array([
            np.hstack([[watched_movie], self.movies_vectors[self.dataset_handler.id2index(watched_movie)]])
            for watched_movie in movies_subset
        ])
        nbrs.fit(movies_with_ids[:, 1:])
        return movies_with_ids[
            nbrs.kneighbors(
                np.array([self.movies_vectors[self.dataset_handler.id2index(movieId)]]), return_distance=False
            )[0],
            0
        ]

recommender = ContentBasedRecommender(dataset_handler)
user_profile = recommender.create_user_profile(user_ratings[170])
recommender.present_user_profile(user_profile)

top = recommender.top(user_profile, topN=5)
recommender.present_recommendations(top)

from evaluator import Evaluator

evaluator = Evaluator(ContentBasedRecommender(dataset_handler))
print("RMSE : ",evaluator.computeRMSE())
#print("MAP  : ",evaluator.computeMAP())