from django.contrib import admin

from rent.models import Rent, RentProduct


class RentProductline(admin.TabularInline):
    model =RentProduct
    readonly_fields = ('user', 'product', 'price')
    can_delete = False
    extra = 0


class RentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name','start_date','end_date', 'phone', 'city', 'status']
    list_filter = ['status']
    readonly_fields = ['user', 'address', 'city','start_date','end_date', 'country', 'phone', 'first_name', 'ip', 'last_name', 'phone']
    can_delete = False
    inlines = [RentProductline]


class RentProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'price']
    list_filter = ['user']


admin.site.register(Rent,RentAdmin)
admin.site.register(RentProduct,RentProductAdmin)
