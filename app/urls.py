from django.urls import path
from app.views import ImageProcessView, ImageDownloadView

urlpatterns = [
    path('uploadImage/', ImageProcessView.as_view(), name='ImageProcessView'),
    path('downloadImage', ImageDownloadView.as_view(), name='download_image'),
]
