from django.contrib import admin
from .models import library_card,books,book_issued
# Register your models here.

admin.site.register(books)
admin.site.register(library_card)
admin.site.register(book_issued)
