# from django.contrib import admin

# from .models import Orders, OrderProduct, Payment


# class OrderProductInline(admin.TabularInline):
#     model = OrderProduct


# class OrdersAdmin(admin.ModelAdmin):
#     list_display = ['order_number', "first_name", "phone", "email", "city", "order_total",
#                     "is_order", "tax", "status", "created_at"]
    
#     list_filter = ['status', 'is_order']
#     search_fields = ["order_number", "first_name", "last_name", "phone", "email"]
#     list_per_page = 20
#     inlines = [OrderProductInline]
    
    
# admin.site.register(Payment)
# admin.site.register(Orders, OrdersAdmin)


from django.contrib import admin
from .models import Orders, OrderProduct, Payment

class OrderProductInline(admin.TabularInline):
   
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'quantity', 'product_price', 'order')
    extra = 0
    

class OrdersAdmin(admin.ModelAdmin):
    list_display = ['order_number', "first_name", "phone", "email", "city", "order_total",
                    "is_order", "tax", "status", "created_at"]
    
    list_filter = ['status', 'is_order']
    search_fields = ["order_number", "first_name", "last_name", "phone", "email"]
    list_per_page = 20
    inlines = [OrderProductInline]

admin.site.register(Payment)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(OrderProduct)
