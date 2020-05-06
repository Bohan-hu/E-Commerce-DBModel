# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.db import models
import django.utils.timezone as timezone

from django.db.models.signals import post_save, post_delete,pre_delete
from django.dispatch import receiver

class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    info = models.ForeignKey('UserLogin', models.CASCADE,verbose_name="选择用户")
    d_address = models.CharField(max_length=60,verbose_name="地址")
    d_name = models.CharField(max_length=20,verbose_name="收货人")
    d_tel = models.CharField(max_length=20,verbose_name="收货电话")
    def username(self):
        return self.info.username
    def __str__(self):
        return self.d_address + ":" + self.d_name + ':' + self.d_tel
    class Meta:
        # managed = False
        db_table = 'address'
        verbose_name_plural = "地址信息管理"


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    info = models.OneToOneField('Userinfo', models.CASCADE)
    cart_total_price = models.FloatField()
    def total_price(self):
        return self.cart_total_price
    def username(self):
        return self.info.user.username
    def items_count(self):
        items = CartInclude.objects.filter(cart__exact=self)
        itemcnt=0
        for item in items:
            itemcnt+=item.num_items
        return itemcnt
    class Meta:
        # managed = False
        db_table = 'cart'
        verbose_name_plural = "购物车管理"
    def __str__(self):
        return self.info.user.username

class CartInclude(models.Model):
    entry_id = models.AutoField(primary_key = True)
    cart = models.ForeignKey('Cart', models.CASCADE)
    product = models.ForeignKey('Product', models.CASCADE)
    add_time = models.DateTimeField(default=timezone.now)
    num_items = models.IntegerField(default=1)
    def __str__(self):
        return str(self.cart.cart_id) + str(self.product.product_id)
    class Meta:
        db_table = 'cart_include'
    def save(self):
    #     # 找到和其所有关联的订单，计算总价
        super(CartInclude, self).save()
        print("saved")
        all_items = CartInclude.objects.filter(cart__exact=self.cart)
        sum = 0
        for item in all_items:
            sum += item.num_items * item.product.product_price
        self.cart.cart_total_price = sum
        print(sum)
        self.cart.save()

@receiver(pre_delete, sender=CartInclude)
def before_delete_cartItem(sender, instance, **kwargs):
    reduced = instance.product.product_price * instance.num_items
    print(reduced)
    instance.cart.cart_total_price -= reduced
    print("cart saved!")
    instance.cart.save()

class OrderInclude(models.Model):
    entry_2_id = models.AutoField(primary_key = True)
    order = models.ForeignKey('Orders', models.CASCADE)
    product = models.ForeignKey('Product', models.CASCADE)
    # final_price = models.FloatField(blank=True, null=True)
    final_quantity = models.IntegerField(default=1)

    class Meta:
        # managed = False
        db_table = 'order_include'
        unique_together = (('order', 'product'))
        verbose_name_plural = "订单关联商品"
    def save(self):
        # 找到和其所有关联的订单，计算总价
        super(OrderInclude, self).save()
        all_items = OrderInclude.objects.filter(order__exact=self.order)
        sum = 0
        for item in all_items:
            sum += item.final_quantity * item.product.product_price
            item.product.storage -= item.final_quantity # 更新库存
            item.product.save()
        self.order.total_money = sum
        print(sum)
        self.order.save()

@receiver(pre_delete, sender=OrderInclude)
def before_delete_orderItem(sender, instance, **kwargs):
    reduced = instance.final_quantity * instance.product.product_price
    instance.order.total_money -= reduced
    instance.order.save()

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    address = models.ForeignKey(Address, models.CASCADE)
    user = models.ForeignKey('UserLogin', models.CASCADE)
    order_status = models.IntegerField()
    delivery_company = models.CharField(max_length=255)
    delivery_id = models.IntegerField()
    payment_time = models.DateTimeField()
    send_time = models.DateTimeField()
    finish_time = models.DateTimeField()
    last_update_time = models.DateTimeField()
    total_money = models.FloatField()
    def __str__(self):
        return "订单#" + str(self.order_id)
    def order_num(self):
        return self.__str__()
    def username(self):
        return self.user.username
    def send_address(self):
        return self.address.d_address + ' / ' + self.address.d_name + ' / ' +self.address.d_tel
    class Meta:
        # managed = False
        db_table = 'orders'
        verbose_name_plural = "订单管理"


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    storage = models.IntegerField()
    catagory = models.ForeignKey('ProductCatagory', models.CASCADE)
    product_name = models.CharField(max_length=255)
    detail = models.TextField()
    last_update = models.DateTimeField()
    product_price = models.FloatField()
    def catagory_name(self):
        return self.catagory.catagory
    def name(self):
        return self.product_name
    def price(self):
        return '￥' + str(self.product_price)
    def sell_count(self):
        items = OrderInclude.objects.filter(product__exact=self)
        sum=0
        for item in items:
            sum+=item.final_quantity
        return sum
    def __str__(self):
        return  self.product_name
    class Meta:
        # managed = False
        db_table = 'product'
        verbose_name_plural = "商品管理"

class ProductCatagory(models.Model):
    catagory_id = models.AutoField(primary_key=True)
    catagory = models.CharField(max_length=20,unique=True)
    def __str__(self):
        return self.catagory
    def product_count(self):
        return Product.objects.filter(catagory__exact=self).count()
    class Meta:
        # managed = False
        db_table = 'product_catagory'
        verbose_name_plural = "商品类型管理"

class ProductPicture(models.Model):
    pict_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, models.CASCADE, blank=True, null=True)
    purl = models.CharField(max_length=255)
    main_pict = models.BooleanField()

    class Meta:
        # managed = False
        db_table = 'product_picture'
        verbose_name_plural = "商品图片管理"



class UserLogin(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20,unique=True,verbose_name="用户名")
    password = models.CharField(max_length=255,verbose_name="密码")
    activate = models.BooleanField()
    userinfo_id = models.IntegerField()
    def email(self):
        return Userinfo.objects.filter(info_id__exact=self.userinfo_id)[0].email
    def phone(self):
        return Userinfo.objects.filter(info_id__exact=self.userinfo_id)[0].u_phone
    def birthdate(self):
        return Userinfo.objects.filter(info_id__exact=self.userinfo_id)[0].birthdate
    def level(self):
        return Userinfo.objects.filter(info_id__exact=self.userinfo_id)[0].level
    def order_count(self):
        return Orders.objects.filter(user__exact=self).count()
    def order_sum(self):
        orders = Orders.objects.filter(user__exact=self)
        sum = 0
        for item in orders:
            sum += item.total_money
        return sum
    def __str__(self):
        return self.username
    class Meta:
        # managed = False
        db_table = 'user_login'
        verbose_name_plural = "用户管理"

class Userinfo(models.Model):
    email = models.CharField(max_length=30,verbose_name="电子邮件")
    u_phone = models.CharField(max_length=20,verbose_name="电话号码")
    register_time = models.DateTimeField(default = timezone.now)
    birthdate = models.DateField(default=timezone.now)
    level = models.IntegerField(default = 1)
    info_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(UserLogin, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
    class Meta:
        # managed = False
        db_table = 'userinfo'

    def save(self):
        # self.register_time =
        super(Userinfo, self).save()
        if len(Cart.objects.filter(info__exact=self)) == 0:
            cart = Cart()
            cart.info = self
            cart.cart_total_price = 0
            cart.save()
        self.user.userinfo_id=self.info_id
        self.user.save()