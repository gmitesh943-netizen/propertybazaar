from django.contrib import admin
from .models import Category, PropertyType, Amenity, Property, PropertyImage, PropertyVideo, BankOffer, Builder

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3

class PropertyVideoInline(admin.TabularInline):
    model = PropertyVideo
    extra = 1

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'category', 'property_type', 'price', 'status', 'featured', 'verified', 'rera_approved')
    list_filter = ('status', 'featured', 'verified', 'rera_approved', 'category', 'property_type', 'listing_type', 'furnishing_status', 'possession_status', 'posted_by')
    search_fields = ('title', 'address', 'city', 'rera_number')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PropertyImageInline, PropertyVideoInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'owner', 'builder', 'category', 'property_type', 'listing_type', 'status')
        }),
        ('Pricing & Area', {
            'fields': ('price', 'area', 'bedrooms', 'bathrooms', 'rooms', 'garage')
        }),
        ('Location', {
            'fields': ('address', 'city', 'state', 'zip_code', 'latitude', 'longitude')
        }),
        ('Property Details', {
            'fields': ('furnishing_status', 'possession_status', 'facing', 'ownership_type', 'posted_by', 'age_of_property', 'total_floors', 'floor_number')
        }),
        ('RERA & Verification', {
            'fields': ('rera_number', 'rera_approved', 'verified', 'featured')
        }),
        ('Media', {
            'fields': ('description', 'floor_plan', 'brochure', 'virtual_tour_url')
        }),
    )

@admin.register(BankOffer)
class BankOfferAdmin(admin.ModelAdmin):
    list_display = ('bank_name', 'interest_rate', 'max_tenure', 'is_recommended', 'order')
    list_editable = ('order', 'is_recommended')
    search_fields = ('bank_name',)

@admin.register(Builder)
class BuilderAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader_name', 'created_at')
    search_fields = ('name', 'leader_name')
