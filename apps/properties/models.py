from django.db import models
from django.conf import settings
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class PropertyType(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Amenity(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class")

    class Meta:
        verbose_name_plural = "Amenities"

    def __str__(self):
        return self.name

class Builder(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='builders/logos/')
    description = models.TextField(blank=True)
    
    # Statistics to match screenshot
    stat1_value = models.CharField(max_length=50, help_text="e.g. 124.3 Mn sqft")
    stat1_label = models.CharField(max_length=100, help_text="e.g. Delivered projects till date")
    stat2_value = models.CharField(max_length=50, help_text="e.g. 150,000+")
    stat2_label = models.CharField(max_length=100, help_text="e.g. Happy families")
    
    # The "Leader" of the company (CEO/Director)
    leader_name = models.CharField(max_length=255)
    leader_designation = models.CharField(max_length=255, help_text="e.g. CEO, Omaxe Limited")
    leader_image = models.ImageField(upload_to='builders/leaders/')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Property(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('sold', 'Sold'),
        ('rented', 'Rented'),
    )
    LISTING_TYPE_CHOICES = (
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
    )
    FURNISHING_CHOICES = (
        ('unfurnished', 'Unfurnished'),
        ('semi-furnished', 'Semi-furnished'),
        ('fully-furnished', 'Fully-furnished'),
    )
    POSSESSION_CHOICES = (
        ('ready_to_move', 'Ready to Move'),
        ('under_construction', 'Under Construction'),
    )
    FACING_CHOICES = (
        ('east', 'East'),
        ('west', 'West'),
        ('north', 'North'),
        ('south', 'South'),
        ('north_east', 'North-East'),
        ('north_west', 'North-West'),
        ('south_east', 'South-East'),
        ('south_west', 'South-West'),
    )
    OWNERSHIP_CHOICES = (
        ('freehold', 'Freehold'),
        ('leasehold', 'Leasehold'),
        ('power_of_attorney', 'Power of Attorney'),
        ('co_operative_society', 'Co-operative Society'),
    )
    POSTED_BY_CHOICES = (
        ('owner', 'Owner'),
        ('agent', 'Agent'),
        ('builder', 'Builder'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties')
    builder = models.ForeignKey(Builder, on_delete=models.SET_NULL, null=True, blank=True, related_name='properties')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='properties')
    property_type = models.ForeignKey(PropertyType, on_delete=models.SET_NULL, null=True, related_name='properties')
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES, default='sale')
    
    description = RichTextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    area = models.IntegerField(help_text="Area in sq ft")
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    rooms = models.IntegerField(default=0)
    garage = models.IntegerField(default=0)
    
    # New Fields
    rera_number = models.CharField(max_length=100, blank=True, null=True)
    rera_approved = models.BooleanField(default=False)
    furnishing_status = models.CharField(max_length=20, choices=FURNISHING_CHOICES, default='unfurnished')
    possession_status = models.CharField(max_length=20, choices=POSSESSION_CHOICES, default='ready_to_move')
    facing = models.CharField(max_length=20, choices=FACING_CHOICES, blank=True, null=True)
    ownership_type = models.CharField(max_length=30, choices=OWNERSHIP_CHOICES, default='freehold')
    posted_by = models.CharField(max_length=20, choices=POSTED_BY_CHOICES, default='owner')
    
    age_of_property = models.PositiveIntegerField(default=0, help_text="Age in years")
    total_floors = models.PositiveIntegerField(default=1)
    floor_number = models.PositiveIntegerField(default=0)
    
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Advanced Media
    floor_plan = models.ImageField(upload_to='property_floor_plans/', blank=True, null=True)
    brochure = models.FileField(upload_to='property_brochures/', blank=True, null=True)
    virtual_tour_url = models.URLField(blank=True, null=True)
    
    amenities = models.ManyToManyField(Amenity, blank=True)
    
    featured = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure slug is unique
            original_slug = self.slug
            queryset = Property.objects.all()
            if self.pk:
                queryset = queryset.exclude(pk=self.pk)
            
            counter = 1
            while queryset.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Properties"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def primary_image_url(self):
        img = self.images.order_by('-is_featured', 'id').first()
        if img:
            return img.get_display_url()
        return PropertyImage.DEFAULT_FALLBACK

class PropertyImage(models.Model):
    DEFAULT_FALLBACK = (
        'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80'
    )

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, help_text='External image URL (used on Render/cloud)')
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.property.title}"

    def get_display_url(self):
        if self.image_url:
            return self.image_url
        if self.image:
            try:
                if self.image.storage.exists(self.image.name):
                    return self.image.url
            except Exception:
                pass
        return self.DEFAULT_FALLBACK

class PropertyVideo(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to='property_videos/')
    
    def __str__(self):
        return f"Video for {self.property.title}"

class BankOffer(models.Model):
    bank_name = models.CharField(max_length=100)
    bank_logo = models.ImageField(upload_to='bank_logos/')
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    max_tenure = models.IntegerField(help_text="Max tenure in years")
    disbursement_days = models.IntegerField(help_text="Days for loan disbursement")
    cash_reward = models.IntegerField(default=0)
    is_recommended = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'bank_name']

    def __str__(self):
        return self.bank_name
