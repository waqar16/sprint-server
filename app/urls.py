from django.urls import path
from app.views import ImageProcessView

urlpatterns = [
    path('uploadImage/', ImageProcessView.as_view(), name='ImageProcessView'),
]
