
from . import views
from django.urls import path

urlpatterns = [

    path('',views.index,name="index"),
    path('home',views.home,name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('logout', views.logout, name="logout"),
    path('userprofile', views.view_profile, name='view_profile'),
    path('updateprofile', views.update_profile, name='update_profile'),
    path('add_movie',views.add_movie,name="add_movie"),
    path('movie_list',views.movie_list,name="movie_list"),
    path('movie_details/<int:movie_id>/',views.movie_details,name="movie_details"),
    path('category/<str:category>/', views.movie_list, name='movie_list_category'),
    path('search/', views.search_movies, name='search_movies'),
    path('movie/<int:movie_id>/update/', views.update_movie, name='update_movie'),
    path('movie/<int:movie_id>/delete/', views.delete_movie, name='delete_movie'),
    path('movie/<int:movie_id>/rate/', views.rate_movie, name='rate_movie'),
    path('movie/<int:movie_id>/review/', views.review_movie, name='review_movie'),
    path('movie/<int:movie_id>/update_rating/', views.update_rating, name='update_rating'),
    path('review/<int:review_id>/update/', views.update_review, name='update_review'),

]