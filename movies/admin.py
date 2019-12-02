from django.contrib import admin
from .models import Movie, Director,Writer,Actor,Rating,Similarity
# Register your models here.


admin.site.register(Movie)
admin.site.register(Director)
admin.site.register(Writer)
admin.site.register(Actor)
admin.site.register(Rating)
admin.site.register(Similarity)