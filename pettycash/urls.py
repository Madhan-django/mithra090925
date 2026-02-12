from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.pettycashExp), name='pettycashExp'),
    path('cashsource',login_required(views.cashsource),name='cashsource'),
    path('newCashSource',login_required(views.addcashsource),name='newcashsource'),
    path('expcategory',login_required(views.expensecategory),name='expcategory'),
    path('balancesheet',login_required(views.balancesheet),name='balancesheet'),
    path('addexpensecategory',login_required(views.addexpensecategory),name='addexpensecategory'),
    path('addexpense',login_required(views.addexpense),name='addexpense'),
    path('balancesheet_pdf',login_required(views.balancesheet_pdf),name='balancesheet_pdf'),
    path('pettycashExp_xl',login_required(views.pettycashExp_xl),name='pettycashExp_xl'),
    path('pettycashvoucher/<exp_id>',login_required(views.pettycashvoucher),name='pettycashvoucher'),


]
