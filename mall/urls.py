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
]