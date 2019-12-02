from collections import defaultdict
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans

from evaluator import Evaluator
from dataset_handler import DatasetHandler

#datasets
datasetmllatest = "ml-latest-small"
dataset1M = "ml-1m"

dataset_handler = DatasetHandler(datasetmllatest)

class CollaborativeFilteringRecommender(object):
    def __init__(self, dataset_handler, neighbours_to_predict=5):
        self.dataset_handler = dataset_handler
        self.movies_vectors = self.dataset_handler.load_movies()
        self.movies_ids = set(self.dataset_handler.id_to_title.keys())
        self.neighbours_to_predict = neighbours_to_predict
    
    def train(self, train_set):
        self.users_ratings = train_set
        self.users_profiles, self.user_id_to_profile_index = self._create_users_profiles(train_set)
        self.movies_watchers = self._get_movies_watchers(train_set)
        self.nbrs = NearestNeighbors(metric='cosine', algorithm='brute')
    
    def top(self, user_profile, topN):
        unrated_movies = np.array([
            (movieId, self.predict_rating(user_profile, movieId))
            for movieId in list(self.movies_ids - user_profile[1])
        ])
        return unrated_movies[np.argpartition(-unrated_movies[:, 1], topN)[:topN], 0]
    
    def predict_rating(self, user_profile, movieId):
        profiles_with_ids = np.array([
            np.hstack([[watcher], self.users_profiles[self.user_id_to_profile_index[watcher]][0]])
            for watcher in self.movies_watchers[movieId]
        ])
        nearest_neighbours = self._cosineKNN(user_profile, profiles_with_ids, self.neighbours_to_predict)
        if not nearest_neighbours:
            return 0.0
        return np.average([self.users_ratings[neighbour][movieId] for neighbour in nearest_neighbours])
    
    def create_user_profile(self, user_ratings):
        mid_rating=2.75
        profile = np.average(
            np.array([
                self.movies_vectors[self.dataset_handler.id2index(movie)]*np.sign(rating - mid_rating)
                for (movie, rating) in user_ratings.items()
            ]),
            weights=(mid_rating-np.array((list(user_ratings.values()))))**2,
            axis=0
        )
        watched_movies = set(user_ratings.keys())
        return (profile, watched_movies)
    
    def present_user(self, user_profile, user_ratings):
        print("User favourite genre:", self.dataset_handler.feature_index2genre(np.argmax(user_profile[0])))
        print("User ratings:")
        for (movieId, rating) in user_ratings.items():
            movie_vector = self.movies_vectors[self.dataset_handler.id2index(movieId)]
            print("{} {}: {}".format(
                self.dataset_handler.id_to_title[movieId],
                self.dataset_handler.movie_vector2genres(movie_vector),
                rating
            ))
    
    def present_recommendations(self, recommendations):
        print( "Recommended movies:")
        for movieId in recommendations:
            movie_vector = self.movies_vectors[self.dataset_handler.id2index(movieId)]
            print("{} {}".format(
                self.dataset_handler.id_to_title[movieId],
                self.dataset_handler.movie_vector2genres(movie_vector)
            ))
    
    def _get_movies_watchers(self, users_ratings):
        movies_watchers = defaultdict(list)
        for (user, user_ratings) in users_ratings.items():
            for movieId in user_ratings.keys():
                movies_watchers[movieId].append(user)
        return movies_watchers
    
    def _create_users_profiles(self, users_ratings):
        users_profiles = []
        user_id_to_profile_index = {}
        for i, (user, user_ratings) in enumerate(users_ratings.items()):
            users_profiles.append(self.create_user_profile(user_ratings))
            user_id_to_profile_index[user] = i
        return users_profiles, user_id_to_profile_index
    
    def _cosineKNN(self, user_profile, profiles_with_ids, k, treshold=20):
        if profiles_with_ids.shape[0] < treshold:
            return []
        self.nbrs.fit(profiles_with_ids[:, 1:])
        return [
            profiles_with_ids[i, 0]
            for i in self.nbrs.kneighbors(np.array([user_profile[0]]), n_neighbors=min(k, len(profiles_with_ids)), return_distance=False)[0]
        
		]

class CollaborativeFilteringWithClusteringRecommender(CollaborativeFilteringRecommender):
    def __init__(self, dataset_handler, neighbours_to_predict=5, clusters=10):
        super(CollaborativeFilteringWithClusteringRecommender, self).__init__(dataset_handler, neighbours_to_predict)
        self.clusters = clusters
    
    def train(self, train_set):
        self.users_ratings = train_set
        self.users_profiles, self.user_id_to_profile_index = self._create_users_profiles(train_set)
        self.kmeans = KMeans(n_clusters=self.clusters).fit(np.array([profile for (profile, _) in self.users_profiles]))
        self.movies_watchers = self._get_movies_watchers(train_set)
        self.nbrs = NearestNeighbors(metric='cosine', algorithm='brute')
    
    def predict_rating(self, user_profile, movieId):
        nearest_group = self.kmeans.predict(np.array([user_profile[0]]))[0]
        profiles_with_ids = np.array([
            np.hstack([[watcher], self.users_profiles[self.user_id_to_profile_index[watcher]][0]])
            for watcher in self.movies_watchers[movieId]
            if self.kmeans.labels_[self.user_id_to_profile_index[watcher]] == nearest_group
        ])
        nearest_neighbours = self._cosineKNN(user_profile, profiles_with_ids, self.neighbours_to_predict)
        if not nearest_neighbours:
            return 0.0
        return np.average([self.users_ratings[neighbour][movieId] for neighbour in nearest_neighbours])

recommender = CollaborativeFilteringWithClusteringRecommender(dataset_handler, 5, 10)
users_ratings = dataset_handler.load_users_ratings()
user_ratings = users_ratings[175]
del users_ratings[1]
recommender.train(users_ratings)
user_profile = recommender.create_user_profile(user_ratings)
recommender.present_user(user_profile, user_ratings)

top = recommender.top(user_profile, topN=5)
recommender.present_recommendations(top)

'''
clusters = [5, 10, 20, 50]
c=[5]
maps, rmses = [], []
for cluster in c:
    evaluator = Evaluator(CollaborativeFilteringWithClusteringRecommender(dataset_handler, 5, cluster))
    rmses.append(evaluator.computeRMSE())
    maps.append(evaluator.computeMAP())
'''

evaluator = Evaluator(CollaborativeFilteringWithClusteringRecommender(dataset_handler, 5, 10))

print("RMSE : ",evaluator.computeRMSE())
#print("MAP : ",evaluator.computeMAP())

#print("Lowest RMSE {} for n_clusters = {}".format(min(rmses), clusters[np.argmin(rmses)]))
#plot(clusters, rmses)

#print(maps)
#print("Highest MAP {} for n_clusters = {}".format(max(maps), clusters[np.argmax(maps)]))
#plot(clusters, maps)