from django.urls import path, include

# API URL patterns
urlpatterns = [
    # API v1 endpoints
    path('v1/', include('api.urls.api_urls')),
]
