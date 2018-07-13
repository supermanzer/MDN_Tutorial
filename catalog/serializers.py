"""
 Defining how our models will be serialized into JSON by our REST API.
"""

from catalog.models import Author, Book, BookInstance, Genre, Language
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Author
    fields = '__all__'

class BookSerialzer(serializers.ModelSerializer):
  class Meta:
    model = Book
    fields = '__all__'

class BookInstanceSerializer(serializers.ModelSerializer):
  class Meta:
    model = BookInstance
    fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
  class Meta:
    model = Genre
    fields = '__all__'

class LanguageSerializer(serializers.ModelSerializer):
  class Meta:
    model = Language
    fields = '__all__'
