from django.contrib import admin
from .models import (
    Block, Floor, Room,
    Vendor, AssetType, Brand,
    Asset, SubAsset
)

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('name', 'school')
    search_fields = ('name', 'school__name')
    list_filter = ('school',)


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ('name', 'block')
    search_fields = ('name', 'block__name')
    list_filter = ('block__school',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'floor')
    search_fields = ('room_number', 'floor__name', 'floor__block__name')
    list_filter = ('floor__block__school',)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'email', 'school')
    search_fields = ('name', 'contact_person', 'phone', 'school__name')
    list_filter = ('school',)


@admin.register(AssetType)
class AssetTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'school')
    search_fields = ('name',)
    list_filter = ('school',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'school')
    search_fields = ('brand_name',)
    list_filter = ('school',)


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('asset_name', 'asset_type', 'room', 'brand', 'condition', 'asset_school', 'is_discarded')
    search_fields = ('asset_name', 'serial_number', 'asset_tag', 'brand')
    list_filter = ('asset_type', 'condition', 'asset_school', 'is_discarded')
    list_select_related = ('room', 'asset_type', 'vendor')


@admin.register(SubAsset)
class SubAssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_asset', 'capacity_or_spec', 'assigned_to', 'condition', 'subasset_school', 'is_discarded')
    search_fields = ('name', 'serial_number', 'sub_asset_tag', 'capacity_or_spec')
    list_filter = ('condition', 'subasset_school', 'is_discarded', 'vendor')
    list_select_related = ('parent_asset', 'assigned_to', 'vendor')
