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
        self.movies_vectors = self.dataset_handler.load_movies() #returns np array in which each element is of the form [0 0 1 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0], '1' representing the genre contained in the movie										
        self.movies_ids = set(self.dataset_handler.id_to_title.keys()) #returns {movieid,title} dict type objects convertred to a list tuple	
        self.neighbours_to_predict = neighbours_to_predict
    
    def train(self, train_set):
        self.users_ratings = train_set
        self.users_profiles, self.user_id_to_profile_index = self._create_users_profiles(train_set) #creates user profile for each user in training set, user profile : array of [-1,1] range value for each genre
        self.movies_watchers = self._get_movies_watchers(train_set) #dict with each element being movieid,[all usrs who watched that movie] pairs
        self.nbrs = NearestNeighbors(metric='correlation', algorithm='brute') 
    
    def top(self, user_profile, topN):
        #list(self.movies_ids - user_profile[1])-list of MovieID that the user didnt watch
        unrated_movies = np.array([
            (movieId, self.predict_rating(user_profile, movieId))
            for movieId in list(self.movies_ids - user_profile[1])
        ])
        return unrated_movies[np.argpartition(-unrated_movies[:, 1], topN)[:topN], 0]
    
    def predict_rating(self, user_profile, movieId):
        profiles_with_ids = np.array([  
            np.hstack([[watcher], self.users_profiles[self.user_id_to_profile_index[watcher]][0]])
            for watcher in self.movies_watchers[movieId]
        ]) #userID and their profile 
        nearest_neighbours = self._cosineKNN(user_profile, profiles_with_ids, self.neighbours_to_predict) #user to user collaberative filtering,list of nearest users
        if not nearest_neighbours:
            return 0.0
        return np.average([self.users_ratings[neighbour][movieId] for neighbour in nearest_neighbours])
    
    def create_user_profile(self, user_ratings): #user profile : array of [-1,1] range value for each genre
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
        return (profile, watched_movies) #profile = how ,mych the user likes a particular genre
    
    def present_user(self, user_profile, user_ratings):
        print("User Favourite Genre :", self.dataset_handler.feature_index2genre(np.argmax(user_profile[0])))
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
        movies_watchers = defaultdict(list) #dict with list type values
        for (user, user_ratings) in users_ratings.items():
            for movieId in user_ratings.keys():
                movies_watchers[movieId].append(user)
        return movies_watchers
    
    def _create_users_profiles(self, users_ratings): # creates profile for each users
        users_profiles = []
        user_id_to_profile_index = {}
        for i, (user, user_ratings) in enumerate(users_ratings.items()): #user_rating will have tuple of movieID and rating , user is userID , enumerate will return index with value in the list , i will store the index
            users_profiles.append(self.create_user_profile(user_ratings))#user_rating will have tuple of movieID and rating
            user_id_to_profile_index[user] = i #dict to keep track of user id value and i (userid,i pairs)
        return users_profiles, user_id_to_profile_index
    
    def _cosineKNN(self, user_profile, profiles_with_ids, k, treshold=20):
        if profiles_with_ids.shape[0] < treshold: #if there are less than threshold users for that movie then set rating to 0
            return []
        self.nbrs.fit(profiles_with_ids[:, 1:])
        return [
            profiles_with_ids[i, 0]
            for i in self.nbrs.kneighbors(np.array([user_profile[0]]), n_neighbors=min(k, len(profiles_with_ids)), return_distance=False)[0]
        
		]

recommender = CollaborativeFilteringRecommender(dataset_handler, 20)
users_ratings = dataset_handler.load_users_ratings() #returns dict inside dict type object, where outside dict : bunch of users, inside dict (each user) : set of movie,rating dict type tuples 
user_ratings = users_ratings[224] #assign 1 element of users_ratings[]
del users_ratings[1]
recommender.train((users_ratings)) #users_ratings passed but this one without chosen user_ratings[" "]
user_profile = recommender.create_user_profile(user_ratings) #creates user profile for the test user, user profile : array of [-1,1] range value for each genre
recommender.present_user(user_profile, user_ratings)

top = recommender.top(user_profile, topN=5)
recommender.present_recommendations(top)

evaluator = Evaluator(CollaborativeFilteringRecommender(dataset_handler, 20))
print("RMSE : ",evaluator.computeRMSE())
#print("MAP : ",evaluator.computeMAP())