from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts import views as account_views
from inventory_app import views as inventory_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inventory_views.dashboard, name='dashboard'),

    path('register/', account_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('products/', inventory_views.product_list, name='product_list'),
    path('products/add/', inventory_views.add_product, name='add_product'),
    path('products/<int:product_id>/', inventory_views.product_detail, name='product_detail'),
    path('products/<int:product_id>/add-sale/', inventory_views.add_sale, name='add_sale'),
]