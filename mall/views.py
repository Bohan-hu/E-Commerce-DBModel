from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import *
# Create your views here.
def product_detail(request, product_id):
    item = Product.objects.get(product_id__exact=product_id)
    entry = {}
    entry['product_id'] = item.product_id
    entry['storage'] = item.storage
    entry['catagory'] = item.catagory.catagory
    entry['product_name'] = item.product_name
    entry['detail'] = item.detail
    entry['price'] = item.product_price
    picts = [item.purl for item in ProductPicture.objects.filter(product__exact=item)]
    entry['pictures'] = picts
    entry['main_picture'] = ProductPicture.objects.filter(product__exact=item).filter(main_pict__exact=True)[0].purl
    return JsonResponse(entry, safe=False)

def product_list(request):
    products = Product.objects.all()
    data = []
    # 订单商品ID+订单商品名+数量
    for item in products:
        entry = {}
        entry['product_id'] = item.product_id
        entry['storage'] = item.storage
        entry['catagory'] = item.catagory.catagory
        entry['product_name'] = item.product_name
        entry['detail'] = item.detail
        entry['price'] = item.product_price
        picts = [ item.purl for item in ProductPicture.objects.filter(product__exact=item)]
        entry['pictures']=picts
        entry['main_picture']=ProductPicture.objects.filter(product__exact=item).filter(main_pict__exact=True)[0].purl
        entry['cart_quantity']=1
        entry['total_price']=entry['price']
        data.append(entry)
    return JsonResponse(data, safe=False)

def product_catagories(request):
    catagories = ProductCatagory.objects.all()
    data = [ item.catagory for item in catagories ]
    return JsonResponse(data, safe=False)

def user_cart(request, user_id):
    ulogin = get_object_or_404(UserLogin, pk=user_id)
    uinfoid = ulogin.userinfo_id
    u_info = get_object_or_404(Userinfo, pk = uinfoid)
    u_cart = Cart.objects.get(info__exact=u_info)
    cart_items = CartInclude.objects.filter(cart__exact=u_cart).order_by('-add_time')
    # context = { 'cart_items' : cart_items, 'u_name': ulogin.username, 'uid':ulogin.user_id }
    # return render(request, 'mall/cart.html', context)
    data = []
    # 订单商品ID+订单商品名+数量
    for item in cart_items:
        entry = {}
        entry['name'] = item.product.product_name
        entry['quantity'] = item.num_items
        entry['price'] = item.product.product_price
        entry['add_time'] = item.add_time
        entry['storage'] = item.product.storage
        data.append(entry)
    return JsonResponse(data, safe=False)

def user_order(request, user_id):
    ulogin = get_object_or_404(UserLogin, pk=user_id)
    u_order = Orders.objects.filter(user__exact=ulogin)
    # order_items = OrderInclude.objects.filter(order__exact=u_order)
    # context = { 'orders' : u_order, 'u_name': ulogin.username, 'uid':ulogin.user_id }
    data = []
    # 订单商品ID+订单商品名+数量
    for item in u_order:
        entry = {}
        entry['order_id']=item.order_id
        entry['address']=item.address.__str__()
        entry['order_status']=item.order_status
        entry['delivery_company']=item.delivery_company
        entry['delivery_id']=item.delivery_id
        entry['payment_time']=item.payment_time
        entry['finish_time']=item.finish_time
        entry['last_update_time']=item.last_update_time
        entry['total_money']=item.total_money
        data.append(entry)
    return JsonResponse(data, safe=False)

def order_detail(request, order_id):
    order_items = OrderInclude.objects.filter(order__exact=order_id)
    # data = serializers.serialize("json", order_items)
    data = []
    # 订单商品ID+订单商品名+数量
    for item in order_items:
        entry = {}
        entry['product_id'] = item.product.product_id
        entry['quantity'] = item.final_quantity
        entry['price'] = item.product.product_price
        data.append(entry)
    # return render(request, 'mall/order_detail.html', context)
    return JsonResponse(data, safe=False)

def login_validate(request):
    pass
