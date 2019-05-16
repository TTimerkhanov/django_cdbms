# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import Book
from books.serializers import BookSerializer


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class HelloView(generics.ListCreateAPIView):
    queryset = Book.nodes.all()
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticated,)
