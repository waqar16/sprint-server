from django.urls import path
from app.views import UploadImageView

urlpatterns = [
    path('uploadImage/', UploadImageView.as_view(), name='UploadImageView'),
]
