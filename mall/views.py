import json

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

# def product_by_catagory(request):
#     products = Product.objects.all()
#     data = []
#     # 订单商品ID+订单商品名+数量
#     for item in products:
#         entry = {}
#         entry['product_id'] = item.product_id
#         entry['storage'] = item.storage
#         entry['catagory'] = item.catagory.catagory
#         entry['product_name'] = item.product_name
#         entry['detail'] = item.detail
#         entry['price'] = item.product_price
#         picts = [ item.purl for item in ProductPicture.objects.filter(product__exact=item)]
#         entry['pictures']=picts
#         entry['main_picture']=ProductPicture.objects.filter(product__exact=item).filter(main_pict__exact=True)[0].purl
#         entry['cart_quantity']=1
#         entry['total_price']=entry['price']
#         data.append(entry)
#     return JsonResponse(data, safe=False)

def product_catagories(request):
    catagories = ProductCatagory.objects.all()
    data = [ item.catagory for item in catagories ]
    return JsonResponse(data, safe=False)

def user_cart(request, user_id):
    ulogin = get_object_or_404(UserLogin, pk=user_id)
    # uinfoid = ulogin.userinfo_id
    # u_info = get_object_or_404(Userinfo, pk = uinfoid)
    u_cart = Cart.objects.get(info__exact=ulogin)
    cart_items = CartInclude.objects.filter(cart__exact=u_cart).order_by('-add_time')
    # context = { 'cart_items' : cart_items, 'u_name': ulogin.username, 'uid':ulogin.user_id }
    # return render(request, 'mall/cart.html', context)
    data = []
    # 订单商品ID+订单商品名+数量
    for item in cart_items:
        entry = {}
        entry['id']=item.entry_id
        entry['product_id']=item.product.product_id
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
        entry['send_time']=item.send_time
        entry['create_time']=item.create_time
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
        entry['product_name'] = item.product.product_name
        entry['product_catagory'] = item.product.catagory.catagory
        entry['quantity'] = item.final_quantity
        entry['price'] = item.product.product_price
        entry['total_price']=item.final_quantity*item.product.product_price
        data.append(entry)
    # return render(request, 'mall/order_detail.html', context)
    return JsonResponse(data, safe=False)



def user_address(request, user_id):
    address = Address.objects.filter(info__exact=user_id)
    # data = serializers.serialize("json", order_items)
    data = []
    # 订单商品ID+订单商品名+数量
    for item in address:
        entry = {}
        entry['address'] = item.d_address
        entry['name'] = item.d_name
        entry['tel'] = item.d_tel
        entry['address_id'] = item.address_id
        data.append(entry)
    # return render(request, 'mall/order_detail.html', context)
    return JsonResponse(data, safe=False)

def user_string_address(request, user_id):
    address = Address.objects.filter(info__exact=user_id)
    # data = serializers.serialize("json", order_items)
    data = []
    # 订单商品ID+订单商品名+数量
    for item in address:
        entry = {}
        entry['value'] = item.address_id
        entry['text'] = item.__str__()
        data.append(entry)
    # return render(request, 'mall/order_detail.html', context)
    return JsonResponse(data, safe=False)


def user_add_address(request):
    if request.method == 'POST':
        print("request", request.POST)
        address=request.POST.get('address',0)
        name=request.POST.get('name',0)
        tel=request.POST.get('tel',0)
        user_id = request.POST.get('userid',0)

        info = UserLogin.objects.get(pk=user_id)
        dict = {  'd_tel': tel, 'd_name':name, 'd_address':address, 'info':info }
        print(dict)
        Address.objects.create(**dict)
        return HttpResponse(status=200)
    else:
        return HttpResponse("Error Method!")

def user_delete_address(request):
    if request.method == 'POST':
        print("request", request.POST)
        Address.objects.filter(address_id__exact=request.POST.get('address_id')).delete()
        return HttpResponse(status=200)
    else:
        return HttpResponse("Error Method!")


#TODO: 以下前端页面还未验证

#TODO: 登录验证
def login_validate(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        userlogin = UserLogin.objects.filter(username__exact=username).filter(password__exact=password)
        ret = {}
        if len(userlogin) == 0:
            ret = { 'success': 0 }
        else:
            ret = { 'success': 1 , 'userid':userlogin[0].user_id }
        return JsonResponse(data=ret, safe=False)

def user_create_order(request):
    # parameter: address_id, user_id, list of products
    # Create a order and set it to
    # set address, user, order status
    # set
    if request.method == 'POST':
        post_data = json.loads(request.body.decode())
        address_id = post_data['address_id']
        product_list = post_data['product_list']
        user_id = post_data['user_id']

        address = Address.objects.get(pk=address_id)
        user = UserLogin.objects.get(pk=user_id)
        # Create the Order Object
        dict = {  'address': address, 'user':user }
        current_order = Orders.objects.create(**dict)
        for product in product_list:
            productObj = Product.objects.get(product_id__exact=product['product_id'])
            dict = { 'product': productObj, 'order': current_order, 'final_quantity': product['quantity']}
            OrderInclude.objects.create(**dict)
        return HttpResponse(status=200)
    else:
        return HttpResponse("Error Method!")

def user_add_cart(request):
    if request.method == 'POST':
        product_id= request.POST.get('product_id',0)
        quantity = request.POST.get('quantity',0)
        user_id = request.POST.get('user_id',0)
        print(user_id,quantity,product_id)

        userlogin = UserLogin.objects.get(pk=user_id)
        cart = Cart.objects.get(info__exact=userlogin)
        product = Product.objects.get(pk=product_id)
        # 先检查购物车内是否已经有相同商品
        cartItem = CartInclude.objects.filter(cart__exact=cart).filter(product__exact=product)
        if len(cartItem) != 0:
            cartItem[0].num_items += int(quantity)
            cartItem[0].save()
        else:
            dict = {  'product': product, 'cart': cart, 'num_items':quantity }
            CartInclude.objects.create(**dict)
        return HttpResponse(status=200)
    else:
        return HttpResponse("Error Method!")

def user_update_cart(request):
    if request.method == 'POST':
        product_id= request.POST.get('product_id',0)
        quantity = request.POST.get('quantity',0)
        user_id = request.POST.get('user_id',0)

        cart = Cart.objects.get(info__exact=user_id)
        product = Product.objects.get(pk=product_id)
        # 先检查购物车内是否已经有相同商品
        cartItem = CartInclude.objects.filter(cart__exact=cart).filter(product__exact=product)
        cartItem[0].num_items = int(quantity)
        cartItem[0].save()
        return HttpResponse(status=200)
    else:
        return HttpResponse("Error Method!")

def user_remove_cart(request):
    if request.method == 'POST':
        post_data = json.loads(request.body.decode())
        # print(post_data)
        for item in post_data:
            id = item['id']
            print(id)
            CartInclude.objects.get(pk=id).delete()
        return HttpResponse(status=200)
    else:
        return HttpResponse("Error Method!")

def user_close_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id',0)
        order = Orders.objects.get(pk=order_id)
        order.order_status = -1
        order.finish_time = timezone.now()
        order.save()
        # 更新商品库存
        orderItems = OrderInclude.objects.filter(order__exact=order)
        for item in orderItems:
            item.product.storage += item.final_quantity
            item.product.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse("Error Method!")

#TODO: 确认订单
def user_confirm_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id',0)
        order = Orders.objects.get(pk=order_id)
        order.order_status = 3
        order.finish_time = timezone.now()
        order.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse("Error Method!")

def user_pay_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id',0)
        order = Orders.objects.get(pk=order_id)
        order.order_status = 1
        order.payment_time = timezone.now()
        order.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse("Error Method!")

def user_profile(request, user_id):
    userlogin = UserLogin.objects.get(user_id=user_id)
    userinfo = Userinfo.objects.get(user__exact=userlogin)
    dict = {}
    dict['password'] = userlogin.password
    dict['email']=userinfo.email
    dict['telephone']=userinfo.u_phone
    dict['birthdate']=userinfo.birthdate
    return JsonResponse(dict, safe=False)
# TODO: 复合查询通用函数