from django.urls import path
from . import views

app_name = 'records'

urlpatterns = [
    path('create/', views.BookCreateView.as_view(), name='create'),
    path('<int:pk>/delete/', views.BookDeleteView.as_view(), name='delete'),
    path('<int:pk>/update/', views.BookUpdateView.as_view(), name='update'),
    path('genre/', views.GenreListView.as_view(), name='genre_list'),
    path('genre/create/', views.GenreCreateView.as_view(), name='genre_create'),
    path('genre/<int:pk>/update/', views.GenreUpdateView.as_view(), name='genre_update'),
    path('genre/<int:pk>/delete/', views.GenreDeleteView.as_view(), name='genre_delete'),
    path('author/', views.AuthorListView.as_view(), name='author_list'),
    path('author/create/', views.AuthorCreateView.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author_delete'),
    path('import/', views.BookImport.as_view(), name='import'),
    path('export/', views.book_export, name='export'),
    path('delete/all/', views.AllBookDeleteView.as_view(), name='delete_all')
]
