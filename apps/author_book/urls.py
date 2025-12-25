from django.urls import path
from .views import *


urlpatterns = [
    path("api/authors/", ListAuthorApiView.as_view()), 
    path("api/authors/created/", CreateAuthorApiView.as_view()),
    path("api/authors/by-id/", ListAuthorByIdApiView.as_view()),
    path("api/authors/with-books/", AuthorWithMinBooksApiView.as_view()),
    path("api/authors/total-books/", AuthorTotalBooksApiView.as_view()),
    path("api/authors/delete/<int:pk>/", AuthorDeleteApiView.as_view()),
    path("api/books/", ListBooksApiView.as_view()),
    path("api/books/created/", CreateBookApiView.as_view()),
    path("api/books/by-id/", RetrieveBooksApiView.as_view()),
    path("api/books/by-genre/", BookFilterByGenreApiView.as_view()),
    path("api/books/rating/<int:pk>/", BookAverageRatingApiView.as_view()),
    path("api/books/delete/<int:pk>/", BookDeleteApiView.as_view())
]
