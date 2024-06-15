# from django.contrib.auth import authenticate
import token

from django.contrib.auth import authenticate
from django.db.models import Count
from rest_framework import status, viewsets, pagination
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.views import APIView

from .models import Author, Publisher, Book
from .serializers import UserSerializer, AuthorSerializer, PublisherSerializer, BookSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"user": serializer.data},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get ('password')
        user = authenticate(username=username, password=password)
        if user:
            token,created =Token.objects.get_or_create(user=user)
            return Response({'token':token.key},status=status.HTTP_200_OK)
        return Response({'error':'invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_fields = ['author', 'publisher']
    pagination_class = pagination.LimitOffsetPagination

class TopAuthorsView(APIView):
    def get(self,request):
        top_authors = Author.objects.annotate(num_books=Count('book')).order_by('-num_books')[:10]
        return Response([{'id': author.id, 'name': author.name, 'num_books': author.num_books} for author in top_authors])

