from django.urls import path
from .views import *

urlpatterns = [
    path("api/lector/", ListLectoresApiView.as_view()),
    path("api/lector/created/", CreateLectorApiView.as_view()),
    path("api/lector/<int:pk>/", RetrieveLectorApiView.as_view()),
    path("api/lector/update/<int:pk>/", UpdateLectorApiView.as_view()),
    path("api/lector/delete/<int:pk>/", DeleteLectorApiView.as_view()),
    path("api/lector/review", TotalLectorReviewApiView.as_view()),
    path("api/lector/active", LectorActiveForYear.as_view(), name="")
]
