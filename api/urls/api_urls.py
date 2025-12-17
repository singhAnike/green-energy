from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from ..views import auth_views, service_views

# Create a router for our API endpoints
router = DefaultRouter()
router.register(r'services', service_views.ServiceViewSet)
router.register(r'appointments', service_views.AppointmentViewSet, basename='appointment')
router.register(r'contact', service_views.ContactMessageViewSet, basename='contact')

# Define the URL patterns for our API
urlpatterns = [
    # Authentication endpoints
    path('auth/register/', auth_views.RegisterView.as_view(), name='auth_register'),
    path('auth/login/', auth_views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', auth_views.LogoutView.as_view(), name='auth_logout'),
    path('auth/me/', auth_views.UserProfileView.as_view(), name='user_profile'),
    
    # Include router URLs
    path('', include(router.urls)),
]
