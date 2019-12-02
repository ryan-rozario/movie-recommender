from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import RequestContext, Context
from .forms import RegistrationForm
from django.shortcuts import redirect
from django.http import Http404
import random


from django.contrib.auth.decorators import login_required


from movies.models import Movie, Director,Writer,Actor,Rating,Similarity


import numpy as np 
import pandas as pd



def get_similar(movie_name,rating,mmm,ratings,ratings2,userRatings,corrMatrix):
    similar_ratings = corrMatrix[movie_name]*(rating-2.5)
    similar_ratings = similar_ratings.sort_values(ascending=False)
    #print(type(similar_ratings))
    return similar_ratings

def func(uid,mmm,ratings,ratings2,userRatings,corrMatrix):
    #print(uid)
    #print(ratings)
    user_rat=ratings2.loc[ratings2['userId'] == str(uid)]
    #print(user_rat)
    user_prof=[]
    for _, row in user_rat.iterrows():
        user_prof.append((row["movie_id"],row["rating"]))
    similar_movies = pd.DataFrame()
    for movie,rating in user_prof:
        similar_movies = similar_movies.append(get_similar(movie,rating,mmm,ratings,ratings2,userRatings,corrMatrix),ignore_index = True)
    #print(similar_movies.sum().sort_values(ascending=False).head(20))
    recommends=pd.DataFrame(similar_movies.sum().sort_values(ascending=False).head(20))
    recommends.reset_index(level=0,inplace=True)
    recommends=recommends.drop(recommends.columns[1],axis=1)
    final=recommends.values

    return final









# Create your views here.

@login_required(login_url='/login/')
def total_view(request,*args,**kwargs):
	rrr=random.randint(2,400)
	queryset = Movie.objects.all()[rrr+0:rrr+40]
	#print(queryset)
	context={
		'mov_all' : queryset,
		'title' : "Movie"
	}
	return render(request,"movies/home.html",context)

@login_required(login_url='/login/')
def genre_view(request,*args,**kwargs):
	g=kwargs.get("genre")
	rrr=random.randint(0,40)
	try:
		queryset = Movie.objects.filter(**{g:True})[0:40]
	except	:
		raise Http404("No MyModel matches the given query.")
	context={
		'mov_all' : queryset,
		'title' : g,
	}
	return render(request,"movies/home.html",context)

@login_required(login_url='/login/')
def movie_detail_view(request,*args,**kwargs):

	user = request.user
	q_m = get_object_or_404(Movie,id=kwargs.get("id"))
	try:
		r=Rating.objects.filter(user_id=user,movie_ids=q_m)
		r=r[0]
	except:
		r=None

	if request.POST:
		stars = request.POST.get('group1')
		#print(stars)

		
		
		if r==None:
			r_add=Rating(user_id =user,movie_ids=q_m,rating=int(stars))
			r_add.save()
		else:
			Rating.objects.filter(user_id=user,movie_ids=q_m).delete()
			r_add=Rating(user_id =user,movie_ids=q_m,rating=int(stars))
			r_add.save()

		return redirect('recom')

		
	try:
		q_a = Actor.objects.filter(movie_ids=q_m)
	except Actor.DoesNotExist:
		q_a = None
	try:
		q_d = Director.objects.filter(movie_ids=q_m)
	except Director.DoesNotExist:
		q_d = None
	try:
		q_w = Writer.objects.filter(movie_ids=q_m)
	except Writer.DoesNotExist:
		q_w = None
	context={
		'm' : q_m,
		'a' : q_a,
		'd' : q_d,
		'w': q_w,
		'r':r
	}
	return render(request,"movies/details.html",context)





def login_user(request):
	template = 'movies/login.html'
	state="Please fill in your credentials"
	log = False
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				state = "Logged in!"
				log = True
				return redirect('total')
			else:
				state = "Not registered user"
		else:
			state = "Incorrect username or password!"
	variables = {
		'state': state,
		'log': log
		}
	return render(request,template, variables)

def reg_user(request):
	dis=""
	state= ""
	template = 'movies/register.html'
	if request.POST:
		form = RegistrationForm(request.POST)
		flag=1
		'''
		try:
			u_dup = User.objects.get(username=form.cleaned_data['username'])
			print(u_dup)
			if u_dup.exists():
				flag=0
		except:
			pass
		try:
			u_dup = User.objects.get(email=form.cleaned_data['email'])
			if u_dup.exists():
				flag=0		
		except:
			pass
		'''
		if form.is_valid() and flag==1:
			if form.cleaned_data['password1']==form.cleaned_data['password2']:
				flag=1	
				try:
					user = User.objects.create_user(
					username = form.cleaned_data['username'],
					password = form.cleaned_data['password1'],
					email = form.cleaned_data['email']
				)
				except:
					dis="User Already Exists"
					flag=0
				if(flag==1):
					return redirect('login')
			else:
				dis="passwords dont match"

		else:
			state = "Incorrect Credentials!"
			
	else:
		form = RegistrationForm()
	variables = {'form':form, 'state':state,'ttt':dis}
	return render(request,template, variables)

def logout_user(request):
	logout(request)
	return redirect('login')


@login_required(login_url='/login/')
def recommendation_view(request):

	username = request.user.id

	#print(username)
	
	mmm = pd.DataFrame(list(Movie.objects.values_list('id','title')))
	
	ratings  = pd.DataFrame(list(Rating.objects.values_list('user_id','movie_ids','rating')))
	

	mmm.columns=["movie_id","title"]

	ratings.columns=['userId', 'movie_id', 'rating']
	ratings['userId']=ratings['userId'].astype(str)

	

	ratings2 = ratings.copy()


	ratings = pd.merge(mmm,ratings)

	

	userRatings = ratings.pivot_table(index=['userId'],columns=['movie_id'],values='rating')

	

	corrMatrix = userRatings.corr(method='pearson')
	corrMatrix.head(100)

	

	

	req=[]
	a=func(username,mmm,ratings,ratings2,userRatings,corrMatrix)
	for i in a:
		req.append(i[0])
	queryset = Movie.objects.filter(pk__in=req)


	context={
		'mov_all' : queryset,
		'title' : "Recommended"
	}
	return render(request,"movies/home.html",context)

