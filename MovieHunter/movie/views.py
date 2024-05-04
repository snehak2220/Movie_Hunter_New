from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Movie_Details, Rating, Review
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request,'index.html')


def home(request):
    return render(request,'home.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not first_name or not last_name or not email or not password1 or not password2:
            messages.error(request, 'All fields are required.')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
        else:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email,
                                            password=password1)
            user.save()
            messages.success(request, 'Registration successful. You can now login.')
            return redirect('/signin')

    return render(request, 'signup.html')
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return render(request,'home.html')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('signin')
    return render(request, 'signin.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required
def view_profile(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'profile.html', context)
@login_required
def update_profile(request):
    user = request.user

    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()
        return redirect('view_profile')

    context = {
        'user': user
    }
    return render(request, 'update_profile.html', context)
@login_required
def add_movie(request):
    if request.method == 'POST':
        title = request.POST['title']
        poster = request.FILES['poster']
        description = request.POST['description']
        release_date = request.POST['release_date']
        actors = request.POST['actors']
        category = request.POST['category']
        trailer_link = request.POST['trailer_link']

        movie = Movie_Details(
            title=title,
            poster=poster,
            description=description,
            release_date=release_date,
            actors=actors,
            category=category,
            trailer_link=trailer_link,
            added_by=request.user,
            created_at=timezone.now()
        )
        movie.save()
        return redirect('movie_list')  # Redirect to movie list page
    return render(request, 'add_movie.html')

def movie_list(request,category=None):
    movies = Movie_Details.objects.filter(added_by=request.user)
    no_movies_added = not movies.exists()
    categories = Movie_Details.objects.values_list('category', flat=True).distinct()
    if category:
        movies = movies.filter(category=category)
    return render(request, 'movie_list.html', {'movies': movies,'categories': categories,'no_movies_added': no_movies_added})

def search_movies(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    movies = Movie_Details.objects.all()

    if query:
        movies = movies.filter(title__icontains=query)
    if category and category != 'All Categories':
        movies = movies.filter(category=category)

    return render(request, 'movie_list.html', {'movies': movies})

def movie_details(request,movie_id):
    movies = Movie_Details.objects.filter(added_by=request.user,id=movie_id)
    return render(request, 'movie_details.html', {'movies': movies})


def update_movie(request, movie_id):
    movie = get_object_or_404(Movie_Details, pk=movie_id)
    if request.method == 'POST':
        movie.title = request.POST['title']
        movie.poster = request.FILES.get('poster')
        movie.description = request.POST['description']
        movie.release_date = request.POST['release_date']
        movie.actors = request.POST['actors']
        movie.category = request.POST['category']
        movie.trailer_link = request.POST['trailer_link']
        movie.save()
        return redirect('movie_list')
    return render(request, 'update_movie.html', {'movie': movie})

def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie_Details, pk=movie_id)
    if request.method == 'POST':
        movie.delete()
        return redirect('movie_list')
    return render(request, 'delete_movie.html', {'movie': movie})

def rate_movie(request, movie_id):
    movie = get_object_or_404(Movie_Details, pk=movie_id)
    if request.method == 'POST':
        # Check if the user has already rated the movie
        existing_rating = Rating.objects.filter(user=request.user, movie=movie)
        if existing_rating.exists():
            # If the user has already rated, redirect back to the movie detail page
            return HttpResponseRedirect(reverse('movie_detail', args=[movie_id]))

        # If the user has not rated yet, add the new rating
        rating_value = float(request.POST['rating'])
        rating = Rating(user=request.user, movie=movie, rating=rating_value)
        rating.save()

        # Redirect back to the movie detail page
        return HttpResponseRedirect(reverse('movie_details', args=[movie_id]))
    return render(request, 'rating.html', {'movie': movie})


def review_movie(request, movie_id):
    movie = get_object_or_404(Movie_Details, pk=movie_id)
    existing_review = Review.objects.filter(user=request.user, movie=movie).exists()

    if request.method == 'POST' and not existing_review:
        review_text = request.POST.get('review')
        if review_text:
            review = Review(user=request.user, movie=movie, review=review_text)
            review.save()
        return HttpResponseRedirect(reverse('movie_details', args=[movie_id]))
    elif existing_review:
        # Redirect to movie detail page if review already exists
        return HttpResponseRedirect(reverse('movie_details', args=[movie_id]))

    return render(request, 'review.html', {'movie': movie})

def update_rating(request, movie_id):
    movie = get_object_or_404(Movie_Details, pk=movie_id)
    # Find the existing rating for the movie by the logged-in user
    existing_rating = Rating.objects.filter(user=request.user, movie=movie).first()
    if request.method == 'POST':
        rating_value = float(request.POST['rating'])
        if existing_rating:
            # Update the existing rating
            existing_rating.rating = rating_value
            existing_rating.save()
        else:
            # If no existing rating, create a new one
            rating = Rating(user=request.user, movie=movie, rating=rating_value)
            rating.save()
        return HttpResponseRedirect(reverse('movie_details', args=[movie_id]))
    return render(request, 'update_rating.html', {'movie': movie, 'existing_rating': existing_rating})

def update_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.method == 'POST':
        review_text = request.POST.get('review')
        review.review = review_text
        review.save()
        return HttpResponseRedirect(reverse('movie_details', args=[review.movie.id]))
    return render(request, 'update_review.html', {'review': review})