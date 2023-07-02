from django.contrib import admin
from .models import Category,stock,Supplier,Order,product_set,Purchase,products,book_set_issue,ind_book

# Register your models here.
admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(stock)
admin.site.register(Order)
admin.site.register(product_set)
admin.site.register(Purchase)
admin.site.register(products)
admin.site.register(book_set_issue)
admin.site.register(ind_book)