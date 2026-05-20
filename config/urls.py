from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api-auth/', include('rest_framework.urls')),
    
    # App URLs
    path('', include('properties.urls')),
    path('user/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('inquiries/', include('inquiries.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('compare/', include('compare.urls')),
    path('visits/', include('visits.urls')),
    path('payments/', include('payments.urls')),
    path('reviews/', include('reviews.urls')),
    path('blog/', include('blog.urls')),
    path('notifications/', include('notifications.urls')),
    path('chat/', include('conversations.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    
    # CKEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Media (demo hosting — uploads may reset on free tier redeploy)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
