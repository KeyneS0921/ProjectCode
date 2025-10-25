from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('success/', views.order_success, name='order-success'),

    path('table/<int:table_id>/menu/', views.table_menu, name='table-menu'),
    path('table/<int:table_id>/order/<int:item_id>/', views.place_order, name='place-order'),
    path('table/<int:table_id>/decrease/<int:item_id>/', views.decrease_item, name='decrease-item'),
    path('table/<int:table_id>/cart/', views.view_cart, name='view-cart'),

    path('merchant/login/', views.merchant_login, name='merchant-login'),
    path('merchant/logout/', views.merchant_logout, name='merchant-logout'),
    path('merchant/dashboard/', views.merchant_dashboard, name='merchant-dashboard'),
    path('merchant/order/<int:order_id>/', views.order_detail, name='order-detail'),
    path('merchant/order/<int:order_id>/complete/', views.complete_order, name='complete-order'),
    path('merchant/add-category/', views.add_category, name='add-category'),
    path('merchant/add-menu-item/', views.add_menu_item, name='add-menu-item'),

    path('qr/<int:table_id>/', views.generate_qr_code, name='generate-qr-code'),
    path('feedback/', views.feedback, name='feedback'),
]