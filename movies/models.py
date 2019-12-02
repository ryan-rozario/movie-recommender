from django.db import models
from django.contrib.auth.models import Permission, User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class Movie(models.Model):
    title   	= models.CharField(max_length=200)
    action      =models.BooleanField(default=False)
    adventure   =models.BooleanField(default=False)
    animation   =models.BooleanField(default=False)
    children    =models.BooleanField(default=False)
    comedy      =models.BooleanField(default=False)
    crime      =models.BooleanField(default=False)
    documentary =models.BooleanField(default=False)
    drama      =models.BooleanField(default=False)
    fantasy      =models.BooleanField(default=False)
    film_noir      =models.BooleanField(default=False)
    horror      =models.BooleanField(default=False)
    musical      =models.BooleanField(default=False)
    mystrey      =models.BooleanField(default=False)
    romance      =models.BooleanField(default=False)
    scifi      =models.BooleanField(default=False)
    thriller      =models.BooleanField(default=False)
    war      =models.BooleanField(default=False)
    western      =models.BooleanField(default=False)
    movie_logo  = models.CharField(max_length=400) 

    
    def __str__(self):
        return self.title

class Director(models.Model):
    name=models.CharField(max_length=200)
    movie_ids 	= models.ForeignKey(Movie,on_delete=models.CASCADE)

class Writer(models.Model):
    name=models.CharField(max_length=200)
    movie_ids 	= models.ForeignKey(Movie,on_delete=models.CASCADE)

class Actor(models.Model):
    name=models.CharField(max_length=200)
    movie_ids 	= models.ForeignKey(Movie,on_delete=models.CASCADE)


class Rating(models.Model):
	user_id   	= models.ForeignKey(User,on_delete=models.CASCADE) 
	movie_ids 	= models.ForeignKey(Movie,on_delete=models.CASCADE)
	rating 	=  models.IntegerField(default=1,validators=[MaxValueValidator(5),MinValueValidator(0)])

class Similarity(models.Model):
    user_id   	= models.ForeignKey(User,on_delete=models.CASCADE) 


