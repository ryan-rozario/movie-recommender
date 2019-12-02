import numpy as np
from movies.models import Movie, Director,Writer,Actor,Rating,Similarity

#print(Movie.objects.all())

import numpy as np
import os
import pandas as pd

movie_filename = "movies.dat"
poster_filename = "movie_poster.csv"


genres = [
    "Action",
    "Adventure",
    "Animation",
    "Children",
    "Comedy",
    "Crime",
    "Documentary",
    "Drama",
    "Fantasy",
    "Film-Noir",
    "Horror",
    "Musical",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Thriller",
    "War",
    "Western"
]

m_cols=['movieId','title','date','blank','link','0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18']
movies_frame = pd.read_csv(os.path.join("data/",movie_filename), sep='|', names=m_cols, usecols=range(24),encoding='latin-1')
#print(movies_frame["0"])
#movies_frame = pd.read_csv(os.path.join("data/",movie_filename), names=["movieId", "title", "genres"], sep="::", engine="python")
poster = pd.read_csv(os.path.join("data/",poster_filename), names=["movieId", "url"], engine="python")
#print(poster["url"][0])




m_total=[]
for _, row in movies_frame.iterrows():
    #for i in gl:
    #    print(i)
    tt=poster.index[poster["movieId"] == int(row["movieId"])].tolist()
    #print(poster(int(row["movieId"])))

    
    a=[]
    for i in range(1,19):
        if row[str(i)]==1:
            a.append(True)
        else:
            a.append(False)

    #a=[1 if genre in gl else 0 for genre in genres]

    #print(a)
    
    if tt!=[]:
        p=poster["url"][tt[0]]
    else:
        p="https://www.valmorgan.com.au/wp-content/uploads/2016/06/default-movie-1-3.jpg"
    m_total.append(Movie(id=(int(row["movieId"])),title=row["title"],action=a[0],adventure=a[1],animation=a[2],children=a[3],comedy=a[4],crime=a[5],documentary =a[6],drama=a[7],fantasy=a[8],film_noir=a[9],horror=a[10],musical=a[11],mystrey=a[12],romance=a[13],scifi=a[14],thriller=a[15],war=a[16],western=a[17],movie_logo=p))
Movie.objects.bulk_create(m_total)


    