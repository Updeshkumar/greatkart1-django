from django.contrib import admin

from .models import Orders, OrderProduct, Payment

admin.site.register(Payment)
admin.site.register(OrderProduct)
admin.site.register(Orders)
