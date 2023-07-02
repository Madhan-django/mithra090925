from django.urls import path
from . import views

urlpatterns = [

    path('supplier/create/',views.supplier_create, name='supplier_create'),
    path('supplier/list/',views.supplier_list, name='supplier_list'),
    path('supplier/update/<int:pk>/',views.supplier_update, name='supplier_update'),
    path('supplier/delete/<int:pk>/',views.supplier_delete, name='supplier_delete'),
    path('purchase/entry/',views.purchase_entry, name='purchase_entry'),
    path('stock/list/',views.stock_list, name='stock_list'),
    path('product/update/<int:pk>/',views.product_update, name='product_update'),
    path('product/delete/<int:pk>/',views.product_delete, name='product_delete'),
    path('category/list',views.category_list,name='category_list'),
    path('category_create',views.category_create,name='category_create'),
    path('category/update/<int:pk>',views.category_update,name='category_update'),
    path('category/delete/<int:pk>',views.category_delete,name='category_delete'),
    path('product_set/create/', views.product_set_create, name='product_set_create'),
    path('product_set_list', views.product_set_list, name='product_set_list'),
    path('product_set/<int:pk>/update/', views.product_set_update, name='product_set_update'),
    path('product_set/<int:pk>/delete/', views.product_set_delete, name='product_set_delete'),
    path('ajax_load_class_prod',views.load_class_prod,name='ajax_load_class_prod'),
    path('reciept_book_set',views.reciept_book_set,name='reciept_book_set'),
    path('products_list',views.products_list,name='products_list'),
    path('product_create',views.product_create,name='product_create'),
    path('purchase_list',views.purchase_list,name='purchase_list'),
    path('purchase/update/<pur_id>',views.purchase_update,name='purchase_update'),
    path('purchase/delete/<pur_id>',views.purchase_delete,name='purchase_delete'),
    path('reciept_ind_book',views.reciept_ind_book,name='reciept_ind_book'),
    path('set_search', views.set_search_view, name='set_search'),
    path('book_set_pdf',views.book_set_pdf,name='book_set_pdf'),
    path('stock_gen_pdf',views.stock_gen_pdf,name='stock_gen_pdf'),
    path('ind_book_pdf',views.ind_book_pdf,name='ind_book_pdf'),
    path('ajax_load_student',views.load_section,name='ajax_load_student'),

]
