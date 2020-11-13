from django.contrib import admin
from webb.models import *

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'uploader', 'quantity', 'price', 'approved')
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'reported')
class CritiqueAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'reported')
class OrderAdmin(admin.ModelAdmin):
    list_display = ('reference_no', 'ordered_at', 'being_delivered', 'received', 'refund_requested')

admin.site.register(Product, ProductAdmin)
admin.site.register(Profile)
admin.site.register(Order, OrderAdmin)
admin.site.register(Address)
admin.site.register(Category)
admin.site.register(OrderProduct)
admin.site.register(Report)
# admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Critique, CritiqueAdmin)
admin.site.register(Hashtag)
admin.site.register(Creator)
admin.site.register(SocialMediaUrl)