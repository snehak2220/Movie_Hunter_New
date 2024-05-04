from django.contrib import admin

from movie.models import Movie_Details, Rating,Review

# Register your models here.
admin.site.register(Movie_Details)
admin.site.register(Rating)
admin.site.register(Review)