from django.urls import path

from . import views

app_name = 'books'
urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('books/<int:pk>', views.BookDetailView.as_view(), name='book'),
    path('books/create', views.BookCreateView.as_view(), name='book_create'),
    path('books/<int:pk>/update', views.BookUpdateView.as_view(), name='book_update'),
    path('books/<int:pk>/delete', views.BookDeleteView.as_view(), name='book_delete'),
    path('authors/', views.author_list, name='author_list'),
    path('authors/<int:pk>', views.author, name='author'),
    path('publishers/', views.publisher_list, name='publisher_list'),
    path('publishers/<int:pk>', views.publisher, name='publisher'),
    path('stores/', views.store_list, name='store_list'),
    path('stores/<int:pk>', views.store, name='store'),

]