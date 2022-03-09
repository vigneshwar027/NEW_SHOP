from django.contrib import admin
from .models import*
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name',('slug')]
    prepopulated_fields= {'slug':('name',)}

admin.site.register(Category,CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','stock','available','created','updated']
    prepopulated_fields= {'slug':('name',)}

admin.site.register(Product,ProductAdmin)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)


admin.site.register(Student)