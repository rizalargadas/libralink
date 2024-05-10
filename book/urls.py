from django.urls import path
from . import views

app_name = 'book'

urlpatterns = [
    path('', views.list_books, name='list_books'),
    path('<uuid:pk>/', views.book_detail, name='book_detail'),
    # path('<uuid:pk>/delete', views.delete_book, name='delete_book'),
    path('<uuid:pk>/edit', views.edit_book, name='edit_book'),
    path('add_book', views.add_book, name='add_book'),
]
