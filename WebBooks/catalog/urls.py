from django.urls import path, include
from .import views
from django.contrib import admin


urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('edit_authors/', views.edit_authors, name='edit_authors'),
    path('authors_add/', views.add_author, name='author_add'),
    path('delete/<int:id>/', views.delete, name='delete'),
]

admin.site.site_header = 'Панель администрирования'
admin.site.index_title = 'Сайт «Мир книг»'

