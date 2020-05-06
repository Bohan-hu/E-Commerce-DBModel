from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *
from django.contrib.auth.models import User, Group
#
# admin.site.unregister(User)
# admin.site.unregister(Group)
# class UserManagement(admin.ModelAdmin):
#     fieldsets = [
#         ('联系方式', {'fields': 'email', 'register_time', 'birthdate', 'level'
#     ]

class UserinfoInline(admin.StackedInline):
    model = Userinfo
    extra = 0

class addressInline(admin.StackedInline):
    model = Address
    extra = 0

@admin.register(UserLogin)
class UserLoginAdmin(admin.ModelAdmin):
    inlines = [UserinfoInline, addressInline]
    list_display = ('Activated','user_id', 'username', 'email', 'phone', 'birthdate', 'level','order_count','order_sum')
    def Activated(self,obj):
        return obj.activate
    Activated.boolean=True
class OrderIncludeInline(admin.StackedInline):
    model = OrderInclude
    extra = 0
@admin.register(Orders)
class OrderInfoAdmin(admin.ModelAdmin):
    inlines = [OrderIncludeInline]
    list_display = ('order_num','user','send_address','delivery_company','delivery_id','total_money')

@admin.register(ProductCatagory)
class ProductCatagoryAdmin(admin.ModelAdmin):
    list_display = ('catagory', 'product_count')

class CartIncludeInline(admin.StackedInline):
    model = CartInclude
    extra = 0

@admin.register(Cart)
class CartInfoAdmin(admin.ModelAdmin):
    inlines = [CartIncludeInline]
    list_display = ('username','total_price','items_count')
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['cart_total_price']

@admin.register(Product)
class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ('catagory_name','name','price','sell_count')

@admin.register(Address)
class AddressInfo(admin.ModelAdmin):
    list_display = ('username', 'd_address', 'd_name', 'd_tel')

# admin.site.register(Address)
# admin.site.register(Cart, CartInfoAdmin)
# admin.site.register(CartInclude)
# admin.site.register(Orders, OrderInfoAdmin)
# admin.site.register(OrderInclude)
# admin.site.register(Product)
# admin.site.register(ProductCatagory)
admin.site.register(ProductPicture)
# admin.site.register(StorageInfo)
# admin.site.register(UserLogin, UserLoginAdmin)
# admin.site.register(Userinfo)

