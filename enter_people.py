import numpy as np
from movies.models import Movie, Director,Writer,Actor,Rating,Similarity
import random

#print(Movie.objects.all())
movie_filename = "movies.dat"

import numpy as np
import os
import pandas as pd


m_cols=['movieId','title','date','blank','link','0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18']
movies_frame = pd.read_csv(os.path.join("data/",movie_filename), sep='|', names=m_cols, usecols=range(24),encoding='latin-1')
fn = pd.read_csv(os.path.join("data/","first-names.txt"))
ln = pd.read_csv(os.path.join("data/","last-names.txt"))
print(fn)

ww=[]
dd=[]
aa=[]
for _, row in movies_frame.iterrows():
    m = Movie.objects.get(id=int(row["movieId"]))
    a=random.randint(1,3)
    for i in range(a):
        b=random.randint(0,88797)
        c=random.randint(0,4943)
        n = str(fn["Aaren"][c]).capitalize()+" "+str(ln["SMITH"][b]).capitalize()
        #print(n)
        aa.append(Actor(name=n,movie_ids=m))
    a=random.randint(1,3)
    for i in range(a):
        b=random.randint(0,88797)
        c=random.randint(0,4943)
        n = str(fn["Aaren"][c]).capitalize()+" "+str(ln["SMITH"][b]).capitalize()
        ww.append(Writer(name=n,movie_ids=m))
    a=random.randint(1,3)
    for i in range(a):
        b=random.randint(0,88797)
        c=random.randint(0,4943)
        n = str(fn["Aaren"][c]).capitalize()+" "+str(ln["SMITH"][b]).capitalize()
        dd.append(Director(name=n,movie_ids=m))


Actor.objects.bulk_create(aa)
Director.objects.bulk_create(dd)
Writer.objects.bulk_create(ww)






