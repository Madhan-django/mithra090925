from django.db import models
from institutions.models import school
from staff.models import staff

# ========= SCHOOL STRUCTURE =========
class Block(models.Model):
    school = models.ForeignKey(school, on_delete=models.CASCADE, related_name='blocks')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.school.name})"


class Floor(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='floors')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Floor {self.name} - {self.block.name}"


class Room(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=50)

    def __str__(self):
        return f"Room {self.room_number} - {self.floor}"


# ========= VENDOR =========

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    school = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# ========= ASSETS =========

class AssetType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    school = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Brand(models.Model):
    brand_name = models.CharField(max_length=100, unique=True)
    school = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return self.brand_name



class Asset(models.Model):
    asset_name = models.CharField(max_length=80)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='assets')
    asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True, blank=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    asset_tag = models.CharField(max_length=100, blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    warranty_end_date = models.DateField(blank=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True, related_name='assets')
    asset_school = models.ForeignKey(school, on_delete=models.CASCADE)
    assign = models.ForeignKey(staff, on_delete=models.SET_NULL,blank=True,null=True)
    condition = models.CharField(max_length=100, default='Good', choices=[
        ('Good', 'Good'),
        ('Average', 'Average'),
        ('Poor', 'Poor'),
        ('Not Working', 'Not Working'),
        ('Transferred','Transferred')
    ])

    is_discarded = models.BooleanField(default=False)
    remark = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return f"{self.asset_name} in {self.room}"


class SubAsset(models.Model):
    parent_asset = models.ForeignKey(
        Asset,
        on_delete=models.SET_NULL,
        related_name='sub_assets',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)
    capacity_or_spec = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    sub_asset_tag = models.CharField(max_length=100, blank=True, null=True)
    assigned_to = models.ForeignKey(staff, on_delete=models.SET_NULL, null=True, blank=True)
    purchase_date = models.DateField(blank=True, null=True)
    warranty_end_date = models.DateField(blank=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True, related_name='sub_assets')
    subasset_school = models.ForeignKey(school, on_delete=models.CASCADE)

    condition = models.CharField(
        max_length=100,
        default='Good',
        choices=[
            ('Good', 'Good'),
            ('Average', 'Average'),
            ('Poor', 'Poor'),
            ('Not Working', 'Not Working'),
            ('Under Repair', 'Under Repair'),
        ]
    )
    is_spare = models.BooleanField(default=False)
    is_discarded = models.BooleanField(default=False)
    remark = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.display_name

    @property
    def display_name(self):
        parent = f" → {self.parent_asset.asset_name}" if self.parent_asset else " (Spare)"
        return f"{self.name} {self.capacity_or_spec or ''}{parent}"



