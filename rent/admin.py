from django.contrib import admin

from rent.models import Rent, RentProduct,ShopCart


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'price','start_date', 'end_date', 'amount']
    list_filter=['user']



class RentProductline(admin.TabularInline):
    model =RentProduct
    readonly_fields = ('user', 'product', 'price','end_date','start_date','amount')
    can_delete = False
    extra = 0


class RentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'city', 'status']
    list_filter = ['status']
    readonly_fields = ['user', 'address', 'city', 'country', 'phone', 'first_name', 'ip', 'last_name', 'phone','total']
    can_delete = False
    inlines = [RentProductline]


class RentProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'price','end_date','start_date','amount']
    list_filter = ['user']


admin.site.register(Rent,RentAdmin)
admin.site.register(RentProduct,RentProductAdmin)
admin.site.register(ShopCart,ShopCartAdmin)

