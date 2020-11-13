from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from datetime import date, datetime, timedelta
from custom_storage import *
from django.urls import reverse
from django_countries.fields import CountryField
# Create your models here.

def get_today_date():
    return date.today()

ps = ProductStorage()
bcs = BlogCritiqueCoverStorage()
pf = ProfileStorage()


## User Management ##
class Profile(models.Model):
    """
    This is the profile of a user
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_verified = models.BooleanField(default=False)
    subscribed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    def verify_email(self):
        self.email_verified = True
        self.save()
    
    def subscribed_to_newsletter(self):
        self.subscribed = True
        self.save()

    def get_shipping_address(self):
        try:
            address = Address.objects.filter(user=self).get(address_types='S')
            return address
        except Address.DoesNotExist:
            return None
    
    def get_billing_address(self):
        try:
            address = Address.objects.filter(user=self).get(address_types='B')
            return address
        except Address.DoesNotExist:
            return None

    def get_order_history(self):
        return Order.objects.filter(user=self).order_by('-ordered_at')

    def get_absolute_url(self):
        return reverse('webb:profile_detail', args=[self.pk])

    def get_following_count(self):
        return ProfileFollowing.objects.filter(following=self).count()

    def get_following_list(self):
        creators = set()
        for c in ProfileFollowing.objects.filter(following=self).select_related('follower'):
            creators.add(c)
        return creators

class Creator(models.Model):
    """
    This is an creator
    """
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    bio = models.TextField()
    bio_img = models.ImageField(storage=pf)
    contact_email = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('webb:creator_info', args=[self.pk])

    def __str__(self):
        return str(self.profile)+"_"+"creator"+"_"+str(self.pk)

    def has_social_media_url(self):
        return self.socialmediaurl_set.first() is None

    def get_social_media_url(self):
        dictionary = {}
        for sm_url in self.socialmediaurl_set.all():
            dictionary[sm_url.brand] = sm_url.url
        return dictionary 

    def get_facebook_url(self):
        dictionary = self.get_social_media_url()
        if 'facebook' in dictionary:
            return dictionary['facebook']
        else:
            return ""

    def get_instagram_url(self):
        dictionary = self.get_social_media_url()
        if 'instagram' in dictionary:
            return dictionary['instagram']
        else:
            return ""
    
    def get_pininterest_url(self):
        dictionary = self.get_social_media_url()
        if 'pininterest' in dictionary:
            return dictionary['pininterest']
        else:
            return ""
    
    def get_twitter_url(self):
        dictionary = self.get_social_media_url()
        if 'twitter' in dictionary:
            return dictionary['twitter']
        else:
            return ""

    def get_followers_count(self):
        return ProfileFollowing.objects.filter(follower=self).count()

class SocialMediaUrl(models.Model):
    CHOICES = [("twitter", "twitter"), ("instagram", "instagram"), 
    ("pininterest","pininterest"), ('facebook', 'facebook')] 
    profile = models.ForeignKey(Creator, on_delete=models.CASCADE)
    brand = models.CharField(max_length=30,choices=CHOICES)
    url = models.CharField(max_length=200)

class Address(models.Model):
    """
    This represents an address
    """
    ADDRESS_TYPES = [('B', 'Billing'),('S', 'Shipping')]
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    address = models.CharField(max_length=1000)
    address_2 = models.CharField(max_length=1000, blank=True, null=True)
    zip_code = models.CharField(max_length=100)
    country = CountryField()
    city = models.CharField(max_length=100)
    address_types = models.CharField(max_length=1, choices=ADDRESS_TYPES)

    def __str__(self):
        dictionary = {'B': 'Billing Address', 'S': 'Shipping Address'}
        return '%s: %s, %s, %s, %s, %s' % (
            dictionary[self.address_types], self.address, self.address_2,
            self.city, str(self.country), self.zip_code)

class ProfileFollowing(models.Model):
    """
    This represents a following model.
    """
    follower = models.ForeignKey(Creator, related_name='follower', on_delete=models.SET_NULL, null=True)
    following = models.ForeignKey(Profile, related_name='following', null=True, on_delete=models.SET_NULL)
    created_at = models.DateField(default=get_today_date)


## Products Management ##
class Category(models.Model):
    """
    This represents a category
    """
    CATEGORY_CHOICES = [("PH", "photo"), ("P", "painting"), ("DP","designer product"), 
    ("S", "stationary"), ("F", "fashion"), ("C", "crossover"), ("LE", "limited edition")]
    name = models.CharField(max_length=2, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

class Product(models.Model):
    """
    This represents a products
    """
    name = models.CharField(max_length=5000)
    uploader = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    available_sizes = models.TextField(blank=True, null=True)
    pic = models.ImageField(storage=ps)
    description = models.TextField()
    price = models.FloatField()
    category = models.ManyToManyField(Category)
    uploaded_date = models.DateField(default=get_today_date)
    tags = models.CharField(max_length=1000, default="", blank=True)
    approved = models.BooleanField(default=False)
    no_sales = models.IntegerField(default=0)
    hide_from_profile = models.BooleanField(default=False)
    enable_das = models.BooleanField(default=False)
    enable_crossover = models.BooleanField(default=False)
    original = models.BooleanField(default=False)
    formats = models.CharField(max_length=30, default='')
    # request_modify = models.BooleanField(defualt=False)
    # request_delete = models.BooleanField(default=False)
    # request_modify_content = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('-uploaded_date',)

    def get_absolute_url(self):
        return reverse('webb:product_detail', kwargs={"pk": self.pk})

    def get_product_url(self):
        return reverse('webb:product_cart', kwargs={"pk": self.pk})

    def __str__(self):
        return self.name + "_" + str(self.pk)
    
    def in_stock(self):
        return self.quantity > 0
    
    def set_approved(self):
        self.approved = True
        self.save()
    
    def get_category(self):
        return str(self.category)
    
    def has_tags(self):
        return len(self.tags) != 0

    def get_tags(self):
        if self.tags is not None and len(self.tags) > 0:
            tags = self.tags.split(", ")
            tags = tags.pop()
            return tags
        return None
    
    def set_hide_from_profile(self):
        self.hide_from_profile = True
        self.save()

    def increase_no_sales(self, quantity):
        self.no_sales += quantity
        self.save()
    
    def get_products_by_name(self):
        return Product.objects.filter(name=self.name)

class Subscription(models.Model):
    max_spots = models.IntegerField(default=20)
    products = models.ManyToManyField(Product)

## Order Management ##
# class Payment(models.Model):
#     """
#     This represents a payment.
#     """
#     stripe_charge_id = models.CharField(max_length=50)
#     user = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
#     amount = models.FloatField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     method = models.CharField(max_length=100)

#     def __str__(self):
#         return self.method + "--" + str(self.amount)

class Coupon(models.Model):
    """
    This represents a coupon.
    """
    code = models.CharField(max_length=20)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
    percentage = models.FloatField()
    expire_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.code

class OrderProduct(models.Model):
    """
    This represent a product in a cart (temporarily)
    """
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    ordered = models.BooleanField()
    quantity = models.IntegerField()

class Order(models.Model):
    """
    This represents an order
    """
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
   # payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True)
    billing_address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True, related_name="billing_address_set")
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True, related_name="shipping_address_set")
    products = models.ManyToManyField(OrderProduct)
    being_delivered = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    ordered_at = models.DateField(blank=True, null=True)
    start_date = models.DateField(default=get_today_date)
    refund_requested = models.BooleanField(default=False)
    refund_request_date = models.DateField()
    refund_received = models.BooleanField(default=False)
    refund_approved = models.BooleanField(default=False)
    reference_no = models.CharField(max_length=30)
    tracking_no = models.CharField(max_length=25, blank=True, null=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

    def request_refund(self, date):
        self.refund_requested = True
        self.request_date = date
        self.save()
    
    def get_status(self):
        # being delivered, delivered, received
        if not being_delivered:
            return "Preparing Product"
        elif being_delivered and not delivered:
            return "Being Delivered"
        elif delivered and not received:
            return "Delivered"
        else:
            return "Received"

    def get_order_price(self):
        price = 0
        for order_product in self.products:
            price += order_product.product.price
        return price

## Blogs Critiques Management ## 
class Hashtag(models.Model):
    tag_text = models.CharField(max_length=100)

    def __str__(self):
        return self.tag_text

    def get_absolute_url(self):
        return reverse('webb:hashtag_detail', args=[self.pk])

class Blog(models.Model):
    """
    This is a blog 
    """
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    text = RichTextUploadingField(blank=True, null=True)
    cover_thumbnail = models.ImageField(storage=bcs, blank=True, null=True)
    created_at = models.DateField(default=get_today_date)
    number_of_likes = models.IntegerField(default=0)
    reported = models.BooleanField(default=False)
    hashtags = models.ManyToManyField(Hashtag)
    hide_from_profile = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('webb:blog_detail', kwargs={"pk": self.pk})

class Critique(models.Model):
    """
    This is a critique of a certain product
    """
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=500)
    text = RichTextUploadingField(blank=True, null=True)
    created_at = models.DateField(default=get_today_date)
    number_of_likes = models.IntegerField(default=0)
    reported = models.BooleanField(default=False)
    cover_thumbnail = models.ImageField(storage=bcs, blank=True, null=True)
    hashtags = models.ManyToManyField(Hashtag)
    hide_from_profile = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('webb:critique_detail', kwargs={"pk": self.pk})

class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField(blank=True, null=True)
    date = models.DateField(get_today_date)
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    class Meta:
        ordering = ['-date',]

## Report Management ##
class Report(models.Model):
    """
    This is a report.
    """
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    created_at = models.DateField(default=get_today_date)
    refund_requested = models.BooleanField(default=False)



