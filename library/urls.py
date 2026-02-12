# library/urls.py
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('books_list/', login_required(views.books_list), name='books_list'),
    path('add_book/', login_required(views.add_book), name='add_book'),
    path('library_cards/', login_required(views.lib_card), name='library_cards'),
    path('gen_lib_card/', login_required(views.gen_lib_card), name='gen_lib_card'),
    path('ajax_load_section/', login_required(views.load_section), name='ajax_load_section'),
    path('ajax_load_student/', login_required(views.load_student), name='ajax_load_student'),
    path('add_book_issued/<int:libbook_id>/', login_required(views.add_book_issued), name='add_book_issued'),
    path('issued_booklist/', login_required(views.issued_booklist), name='issued_booklist'),
    path('book_return/<int:libbook_id>/', login_required(views.book_return), name='book_return'),
    path('search_issued/', login_required(views.search_issued), name='search_issued'),
    path('print_card/<int:libcard_id>/', login_required(views.print_card), name='print_card'),
]











