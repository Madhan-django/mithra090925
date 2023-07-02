from django.urls import path
from library import views


urlpatterns=[
    path('books_list',views.books_list,name='books_list'),
    path('add_book',views.add_book,name='add_book'),
    path('library_cards',views.lib_card,name='library_cards'),
    path('gen_lib_card',views.gen_lib_card,name='gen_lib_card'),
    path('ajax_load_section',views.load_section,name='ajax_load_section'),
    path('ajax_load_student',views.load_student,name='ajax_load_student'),
    path('add_book_issued/<libbook_id>',views.add_book_issued,name='add_book_issued'),
    path('issued_booklist',views.issued_booklist,name='issued_booklist'),
    path('book_return/<libbook_id>', views.book_return, name='book_return'),
    path('search_issued',views.search_issued,name='search_issued'),
    path('print_card/<libcard_id>',views.print_card,name='print_card'),
]