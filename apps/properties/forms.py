from django import forms
from .models import Property, PropertyImage, PropertyVideo, Category, PropertyType, Amenity

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'category', 'property_type', 'description', 
            'price', 'area', 'bedrooms', 'bathrooms', 'rooms', 'garage',
            'address', 'city', 'state', 'zip_code', 'amenities', 'status'
        ]
        widgets = {
            'amenities': forms.CheckboxSelectMultiple(),
        }

class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image', 'is_featured']

class PropertyVideoForm(forms.ModelForm):
    class Meta:
        model = PropertyVideo
        fields = ['video']

PropertyImageFormSet = forms.inlineformset_factory(
    Property, PropertyImage, form=PropertyImageForm, extra=5, can_delete=True
)

PropertyVideoFormSet = forms.inlineformset_factory(
    Property, PropertyVideo, form=PropertyVideoForm, extra=1, can_delete=True
)
