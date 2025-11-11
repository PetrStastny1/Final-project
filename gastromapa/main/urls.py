# ... existing code ...
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views

# REST Framework Router
router = DefaultRouter()
router.register(r'businesses', views.BusinessViewSet, basename='business')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'reviews', views.ReviewViewSet, basename='review')

urlpatterns = [
    # HTML Views
    path('', views.home, name='home'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('business/', views.business_list, name='business_list'),
    path('business/<int:id>/', views.business_detail, name='business_detail'),
    path('business/<int:id>/add_review/', views.add_review, name='add_review'),
    path('business/<int:id>/delete/', views.business_delete, name='business_delete'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('search/', views.business_search, name='business_search'),
    path('add_business/', views.add_business, name='add_business'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/user_login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('media/', views.media_list, name='media_list'),

    # API Views (using DRF router)
    path('api/', include(router.urls)),

    # Legacy API Endpoints (if needed)
    path('api/businesses/', views.api_business_list, name='api_business_list'),
    path('api/businesses/<int:id>/', views.api_business_detail, name='api_business_detail'),
    path('api/reviews/', views.api_review_list, name='api_review_list'),
    path('api/categories/', views.api_category_list, name='api_category_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)