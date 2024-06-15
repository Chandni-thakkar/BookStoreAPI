from rest_framework import serializers

from django.contrib.auth.models import User

from .models import Author, Publisher, Book

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    publisher = PublisherSerializer()

    class Meta:
        model = Book
        fields = '__all__'

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        publisher_data = validated_data.pop('publisher')
        author_instance, _ = Author.objects.get_or_create(**author_data)
        publisher_instance, _ = Publisher.objects.get_or_create(**publisher_data)
        book = Book.objects.create(author=author_instance, publisher=publisher_instance, **validated_data)
        return book
