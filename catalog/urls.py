"""
 catalog/urls.py
---------------------------------------------------------------
 Url routing logic for the catalogs application.
"""
from django.urls import path
from catalog import views

# Namespaces are a honking great idea - Zen of Python
app_name='catalog'

urlpatterns = [
  path('', views.index, name='index'),
  path('book/<int:id>/<slug:slug>',views.BookDetailView.as_view(), name='book-detail'),
  path('book/',views.BookListView.as_view(),name='books'),
  path('author/', views.AuthorListView.as_view(), name='authors'),
  path('author/<int:id>/<slug:slug>', views.AuthorDetailView.as_view(), name='author-detail'),
  path('language/', views.LangListView.as_view(), name='languages'),
  path('language/<int:pk>/<str:language>' ,views.LangDetailView.as_view(), name='language-detail'),
  path('genre/', views.GenreListView.as_view(), name='genre-list'),
  path('genre/<int:pk>/<str:genre>', views.GenreDetailView.as_view(), name='genre-detail'),
  path('mybooks/', views.LoannedBooksByUserListView.as_view(), name='my-borrowed-books'),
  path('all-books/', views.AllBorrowedBooksListView.as_view(), name='all-books'),
  path('check-in/<uuid:pk>/', views.BorrowedBookDetailView.as_view(), name='check-in'),
  path('check-out/<uuid:pk>/', views.CheckoutBookInstance.as_view(), name='check-out'),
]
