
from django.urls import path
from django.urls import path, include
from rest_framework import routers
from .views import RegisterView, LoginView, AuthorViewSet, PublisherViewSet, BookViewSet, TopAuthorsView

router = routers.DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='authors')
router.register(r'publishers', PublisherViewSet, basename='publishers')
router.register(r'books', BookViewSet, basename='books')

urlpatterns = [
    path('register/', RegisterView.as_view(),name='register'),
    path('login/', LoginView.as_view(),name='login'),
    path('topauthors/', TopAuthorsView.as_view(),name='top-authors'),
    path('', include(router.urls)),
]
