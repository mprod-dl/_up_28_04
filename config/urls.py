from django.contrib import admin
from django.urls import path, include
from general.views import *
from config import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view_products, name='view_products'),
    path('product/<int:id>/', view_product_by_id, name='view_product_by_id'),
    path('by_category/<int:category_id>/', view_products_by_category, name='view_products_by_category'),
    path('by_tag/<int:tag_id>/', view_products_by_tag, name='view_products_by_tag'),

    path('add_product/', add_product, name='add_product'),
    path('add_category/', add_category, name='add_category'),
    path('add_tag/', add_tag, name='add_tag'),
    
    path('edit_product/<int:id>/', edit_product, name='edit_product'),
    
    path('categories_and_tags/', view_categories_and_tags, name="view_categories_and_tags"),
    
    path('cart/', view_cart, name="view_cart"),
    path('cart/add/<int:product_id>/', add_to_cart, name="add_to_cart"),
    path('cart/remove/<int:product_id>/', remove_from_cart, name="remove_from_cart"),
    path('cart/clear/', clear_cart, name="clear_cart"),
    
    path('profile/', view_profile, name="view_profile"),
    
    path('api/', include('api_general.urls')), # API
    
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('forbidden/', forbidden, name="forbidden"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
