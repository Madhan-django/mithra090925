from django import forms
from .models import Block,Floor,Room,Vendor,AssetType,Asset,SubAsset,Brand


class New_BlockForm(forms.ModelForm):
    class Meta:
        model = Block
        fields = '__all__'

        widgets = {
            'school': forms.HiddenInput(),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'New Building Name',
            }),
        }

        labels = {
            'name': 'Building Name',
        }
class New_FloorForm(forms.ModelForm):
    class Meta:
        model = Floor
        fields = '__all__'
        widgets = {
            'block': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels ={
            'name':'Floor Name'
        }

class Update_FloorForm(forms.ModelForm):
    class Meta:
        model = Floor
        fields = '__all__'
        widgets = {
            'block': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels ={
            'name':'Floor Name'
        }



class New_RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields ='__all__'

class Update_RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields ='__all__'
        widgets = {
            'floor':forms.HiddenInput(),
            'room_number':forms.TextInput(attrs={'class':'form-control'})

        }

class New_BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields ='__all__'

        widgets= {
            'school':forms.HiddenInput(),
            'brand_name':forms.TextInput(attrs={'class':'form-control'})
        }

class New_VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields ='__all__'

        widgets = {
            'school': forms.HiddenInput(),

        }



class New_AssetTypeForm(forms.ModelForm):
    class Meta:
        model = AssetType
        fields ='__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'floatingInput',
                'placeholder': 'Enter Asset Type Name',
                'aria-describedby': 'floatingInputHelp',
            }),
            'school': forms.HiddenInput(),  # assuming this field should be hidden
        }

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = [
            'asset_name', 'room', 'asset_type', 'brand', 'serial_number',
            'asset_tag', 'purchase_date', 'warranty_end_date', 'vendor',
            'asset_school', 'condition', 'is_discarded','assign','remark'
        ]
        widgets = {
            'asset_name': forms.TextInput(attrs={'class': 'form-control'}),
            'room': forms.Select(attrs={'class': 'form-control'}),
            'asset_type': forms.Select(attrs={'class': 'form-control'}),
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'asset_tag': forms.TextInput(attrs={'class': 'form-control'}),
            'purchase_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'warranty_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'vendor': forms.Select(attrs={'class': 'form-control'}),
            'asset_school': forms.Select(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'is_discarded': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'assign':forms.Select(attrs={'class':'form-control'}),
            'remark': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Remark'}),
        }

class SubAssetForm(forms.ModelForm):
    class Meta:
        model = SubAsset
        fields = [
            'parent_asset', 'name', 'capacity_or_spec', 'serial_number', 'sub_asset_tag',
            'assigned_to', 'purchase_date', 'warranty_end_date', 'vendor',
            'subasset_school', 'condition', 'is_spare', 'is_discarded','remark'
        ]
        widgets = {
            # 👇 Replace normal select with searchable one
            'parent_asset': forms.Select(
                       attrs={
                               'class': 'form-control select2',
                               'data-placeholder': 'Search or select parent asset...'
                            }

            ),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., RAM, HDD, Adapter'}),
            'capacity_or_spec': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 16GB DDR4, 500GB SSD'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Serial Number'}),
            'sub_asset_tag': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Tag ID'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'purchase_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'warranty_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'vendor': forms.Select(attrs={'class': 'form-control'}),
            'subasset_school': forms.Select(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'is_spare': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_discarded': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'remark': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Remark'}),
        }

    def __init__(self, *args, **kwargs):
        asset = kwargs.pop('asset', None)
        school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)

        if asset:
            self.fields['parent_asset'].initial = asset
            self.fields['parent_asset'].disabled = True

        if school:
            self.fields['subasset_school'].initial = school
            self.fields['subasset_school'].disabled = True

        self.fields['is_spare'].label = "Mark as Spare"
        self.fields['is_discarded'].label = "Discarded / Not in Use"

class SpareForm(forms.ModelForm):
    class Meta:
        model = SubAsset
        fields = [
            'parent_asset', 'name', 'capacity_or_spec', 'serial_number', 'sub_asset_tag',
            'assigned_to', 'purchase_date', 'warranty_end_date', 'vendor',
            'subasset_school', 'condition', 'is_spare', 'is_discarded','remark',
        ]
        widgets = {
            'parent_asset': forms.Select(attrs={'class': 'form-control select2', 'data-placeholder': 'Select Parent Asset'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity_or_spec': forms.TextInput(attrs={'class': 'form-control'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'sub_asset_tag': forms.TextInput(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control select2'}),
            'purchase_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'warranty_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'vendor': forms.Select(attrs={'class': 'form-control select2'}),
            'subasset_school': forms.Select(attrs={'class': 'form-control select2'}),
            'condition': forms.Select(attrs={'class': 'form-control select2'}),
            'is_spare': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_discarded': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'remark': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Remark'}),
        }

    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)
        if school:
            self.fields['parent_asset'].queryset = Asset.objects.filter(asset_school=school)
            self.fields['subasset_school'].initial = school
            self.fields['subasset_school'].disabled = True
