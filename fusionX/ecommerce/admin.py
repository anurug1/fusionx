from django.contrib import admin
from .models import *

class ProductCommentInline(admin.StackedInline):
    model = ProductComment
    
class ProductTabularInline(admin.TabularInline):
    model = ProductComment
    extra = 1
#Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display= ['id','name','slug','price','amount','brand','show_image']
    list_filter=['brand']
    search_fields=['pId','name']
    prepopulated_fields = {'slug': ('name',)} 
    inlines = [ProductTabularInline]


admin.site.register(Brand)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductComment)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Size)

