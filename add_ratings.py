import numpy as np
import os
import pandas as pd


from movies.models import Movie, Director,Writer,Actor,Rating,Similarity
from django.contrib.auth.models import User


rating_filename = "ratings.dat"


rating_frame = pd.read_csv(os.path.join("data/",rating_filename), names=["userId", "movieId", "rat","timestamp"], sep="\t", encoding='latin-1')
r=[]
for _, row in rating_frame.iterrows():
    
    u = User.objects.get(username=str(row["userId"]))
    m = Movie.objects.get(id=int(row["movieId"]))
    r.append(Rating(user_id =u,movie_ids=m,rating=int(row["rat"])))
    
Rating.objects.bulk_create(r)