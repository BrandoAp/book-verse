from django.urls import path
from .views import *

urlpatterns = [
    path("api/reviews/created/", CreateReviewApiView.as_view()),
    path("api/reviews/", ListReviewsApiView.as_view()),
    path("api/reviews/<int:pk>/", RetriveReviewsApiView.as_view()),
    path("api/reviews/<int:pk>/update/", UpdateReviewApiView.as_view()),
    path("api/reviews/<int:pk>/delete/", DeleteReviewApiView.as_view()),
    path("api/reviews/<int:book_id>/by-book/", ReviewsByBookApiView.as_view()),
    path("api/reviews/<int:user_id>/by-user/", ReviewsByUserAPIView.as_view()),
]
