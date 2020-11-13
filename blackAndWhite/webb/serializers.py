from rest_framework import serializers
from webb.models import *
from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('pk', 'name', 'creator', 'quantity', 'available_sizes', 'pic', 'description', 
        'price', 'category', 'uploaded_date', 'tags', 'approved', 'no_sales', 'hide_from_profile')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('pk', 'user', 'email_verified', 'subscribed')

class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = ('pk', 'profile', 'name', 'bio', 'bio_img', 'contact_email', 'social_media_url', 'skills')

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('pk', 'user', 'address', 'zip_code', 'country', 'city', 'address_types')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk', 'name')

# class PaymentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         fields = ('pk', 'stripe_charge_id', 'user', 'amount', 'timestamp')

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('pk', 'user', 'payment', 'coupon', 'billing_address', 'shipping_address', 'products', 'being_delivered', 'received', 'ordered_at', 
        'start_date', 'refund_requested', 'refund_request_date', 'refund_received', 'refund_request_reason', 'refund_approved', 'reference_no', 'tracking_no')

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ('pk', 'product', 'user', 'quantity', 'ordered')

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('pk', 'user', 'title', 'text', 'created_at', 'number_of_likes', 'reported')

class CritiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Critique
        fields = ('pk', 'user', 'product', 'title', 'text', 'created_at', 'number_of_likes', 'reported')


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('pk', 'product', 'user', 'quantity', 'created_at', 'refund_requested')

