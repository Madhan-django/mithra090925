# automate/urls.py
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('blocks',login_required(views.block_list),name='block_list'),
    path('new_block',login_required(views.add_block),name='new_block'),
    path('edit_block/<block_id>',login_required(views.edit_block),name='edit_block'),
    path('delete_block/<block_id>',login_required(views.delete_block),name='delete_block'),
    path('floors',login_required(views.floor_list),name='floor_list'),
    path('new_floor',login_required(views.add_floor),name='new_floor'),
    path('edit_floor/<floor_id>', login_required(views.edit_floor), name='edit_floor'),
    path('delete_floor/<floor_id>',login_required(views.delete_floor),name='delete_floor'),
    path('rooms', login_required(views.room_list), name='room_list'),
    path('add_newbrand',login_required(views.add_newbrand),name='add_newbrand'),
    path('new_room',login_required(views.add_room),name='new_room'),
    path('update_room/<room_id>',login_required(views.update_room),name='update_room'),
    path('delete_room/<room_id>', login_required(views.delete_room), name='delete_room'),
    path('vendors',login_required(views.vendor_list),name='vendor_list'),
    path('new_vendor',login_required(views.add_vendor),name='new_vendor'),
    path('update_vendor/<vendor_id>',login_required(views.update_vendor),name='update_vendor'),
    path('delete_vendor/<vendor_id>',login_required(views.delete_vendor),name='delete_vendor'),
    path('asset_type',login_required(views.assettypes_list),name='asset_type'),
    path('new_assettype',login_required(views.add_assettype),name='new_assettype'),
    path('update_assettype/<asset_id>',login_required(views.update_assettype),name='update_assettype'),
    path('delete_assettype/<asset_id>',login_required(views.delete_assettype),name='delete_assettype'),
    path('',login_required(views.asset),name='asset'),
    path('add_asset',login_required(views.add_asset),name='add_asset'),
    path('update_asset/<asset_id>',login_required(views.update_asset),name='update_asset'),
    path('delete_asset/<asset_id>',login_required(views.delete_asset),name='delete_asset'),
    path('sub_assets',login_required(views.sub_assets),name='sub_assets'),
    path('subasset/add/', login_required(views.add_subasset), name='add_spare_subasset'),
    path('subasset/add/<int:asset_id>/', views.add_subasset, name='add_subasset'),
    path('add_subasset/<asset_id>/',login_required(views.add_subasset),name='add_subasset'),
    path('update_subasset/<subasset_id>',login_required(views.update_subasset),name='update_subasset'),
    path('update_spare/<subasset_id>',login_required(views.update_spare),name='update_spare'),
    path('delete_subasset/<subasset_id>',login_required(views.delete_subasset),name='delete_subasset'),
    path('brand_list',login_required(views.brand_list),name='brand_list'),
    path('brand_delete/<brand_id>',login_required(views.brand_delete),name='brand_delete'),
    path('get_subassets/<int:asset_id>/',login_required(views.get_subassets), name='get_subassets'),
    path('spareslist',login_required(views.spareslist),name='spareslist'),
    path('import_assets',login_required(views.import_assets),name='import_assets'),
    path('download_asset_template',login_required(views.download_asset_template),name='download_asset_template')



]











