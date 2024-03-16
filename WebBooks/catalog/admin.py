from django.contrib import admin
from .models import Author, Book, Genre, Language, Publisher, Status, BookInstance

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Publisher)
admin.site.register(Status)
admin.site.register(BookInstance)