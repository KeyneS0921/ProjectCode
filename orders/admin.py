from django.contrib import admin

from django.contrib import admin
from .models import Restaurant, Table, MenuCategory, MenuItem, Order, OrderItem

admin.site.register(Restaurant)
admin.site.register(Table)
admin.site.register(MenuCategory)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderItem)