from django.urls import path

from books.views import HelloView

urlpatterns = [
    path('hello', HelloView.as_view(), name='hello')
]
