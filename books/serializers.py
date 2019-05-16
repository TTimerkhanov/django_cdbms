from rest_framework import serializers

from authors.serializers import AuthorSerializer


class BookSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=40)
    author = AuthorSerializer(many=True)
