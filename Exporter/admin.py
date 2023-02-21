from django.contrib import admin
from .models import Warehouse, Type, Request, WarehouseType, Order, Payment

class WarehouseTypeInline(admin.TabularInline):
    model = WarehouseType

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    inlines = [WarehouseTypeInline]


admin.site.register(Type)
admin.site.register(Request)
admin.site.register(Order)
admin.site.register(Payment)
