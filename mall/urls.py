from django.urls import path

from . import views
app_name = 'mall'
urlpatterns = [
    # ex: /polls/
    # path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('user_cart/<int:user_id>', views.user_cart, name='user_cart'),
    path('user_order/<int:user_id>', views.user_order, name='user_order'),
    path('order_detail/<int:order_id>', views.order_detail, name='order_detail'),
    path('products', views.product_list, name='product_list'),
    path('user_address/<int:user_id>', views.user_address, name='user_address'),
    path('user_add_address/',views.user_add_address, name='user_add_address'),
    path('user_delete_address/',views.user_delete_address, name='user_delete_address'),
    path('user_create_order/',views.user_create_order, name='user_create_order'),
    path('user_add_cart/',views.user_add_cart, name='user_add_cart'),
    path('user_update_cart/',views.user_update_cart, name='user_update_cart'),
    path('user_remove_cart/',views.user_remove_cart, name='user_remove_cart'),
    path('user_close_order/',views.user_close_order, name='user_close_order'),
    path('user_confirm_order/',views.user_confirm_order, name='user_confirm_order'),
]