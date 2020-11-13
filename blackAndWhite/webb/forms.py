from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from webb.models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django_countries.fields import CountryField


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Please remember to verify your email afterwards.')
    class Meta:
        model = User
        fields = [
            "username", 
            "password1", 
            "password2", 
            "email"
        ]

class ProductModalForm(forms.ModelForm):
    TAGS = {
        ("", "--"),
        ("NEW", 'NEW',),
        ("CREATOR'S PICK", "CREATOR'S PICK")
    }
    category = forms.ModelMultipleChoiceField(
            queryset=Category.objects,
            widget=forms.CheckboxSelectMultiple,
            required=True)

    tags = forms.CharField(max_length=100, widget=forms.Select(choices=TAGS))
    
    class Meta:
        model = Product
        fields = [
            "name", 
            "quantity", 
            "pic", 
            "description", 
            "price", 
            "category", 
            "enable_das", 
            "enable_crossover", 
            'tags', 
            'available_sizes', 
            'original',
            'formats'
        ]
         
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Product Name'})
        self.fields['description'].widget.attrs.update({'placeholder':'Product Description'})
        self.fields['pic'].required = True

class BlogModalForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Blog
        fields = (
            "title", 
            'cover_thumbnail', 
            'text'
        )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Title Of Blog'})

class CritiqueModalForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Critique
        fields = (
            "title", 
            "product", 
            'cover_thumbnail', 
            'text'
        )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Title Of Critique'})

class CreatorModalForm(forms.ModelForm):
    class Meta:
        model = Creator
        fields = (
            'bio', 
            'bio_img', 
            'contact_email',
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bio'].widget.attrs.update({'placeholder': 'Type out your bio here'})
        self.fields['contact_email'].widget.attrs.update({'placeholder': 'Enter your contact email'})

class AddressModalForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = (
            'address',
            'address_2',
            'zip_code',
            'city',
            'country'
        )

class RefundModalForm(forms.ModelForm):
    class Meta:
        model = Refund
        fields = (
            'reason',
            'email'
        )

class CheckoutForm(forms.Form):
    PAYMENT_CHOICES = (
        ('S', 'Stripe'),
        ('P', 'PayPal'),
        ('C', 'Credit Card')
    )
    shipping_address = forms.CharField(required=True)
    shipping_address2 = forms.CharField(required=False)
    shipping_city = forms.CharField(required=True)
    shipping_country = CountryField(blank_label='select country').formfield()
    shipping_zip = forms.CharField(required=False)

    billing_address = forms.CharField(required=True)
    billing_address2 = forms.CharField(required=False)
    billing_city = forms.CharField(required=True)
    billing_country = CountryField(blank_label='select country').formfield()
    billing_zip = forms.CharField(required=False)

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

