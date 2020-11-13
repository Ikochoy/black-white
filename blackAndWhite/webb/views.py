from django.shortcuts import render
from django.views.generic import TemplateView
from webb.models import *
from webb.forms import *
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from rest_framework import viewsets          
from .serializers import *
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .email_tokens import email_verification_token
# Create your views here.


## RENDER TEMPLATES ##
def home(request):
    return render(request, "home.html", {})

## PROFILE ##
class ProfileDetailView(DetailView):
    model = Profile
    template_name = "profile_detail.html"

def change_email(request):
    user = request.user
    user.email = request.GET.get('email')
    user.save()
    profile = Profile.objects.get(user=user)
    profile.email_verified = False
    profile.save()
    return HttpResponse('success')

## PRODUCTS ##

class ProductByCategoryListView(ListView):
    model = Product
    paginate_by = 10
    template_name = "products/product.html"

    def get_queryset(self):
        if self.kwargs['category_name'] != 'AP':
            return Category.objects.get(name=self.kwargs['category_name']).product_set.all()
        else:
            return Product.objects.all()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        if self.kwargs['category_name'] == 'AP':
            category = 'ALL PRODUCTS'
        elif self.kwargs['category_name'] == 'PH':
            category = 'PHOTOS'
        elif self.kwargs['category_name'] == 'P':
            category = 'PAINTINGS'
        elif self.kwargs['category_name'] == 'DP':
            category = 'DESIGNER PRODUCTS'
        elif self.kwargs['category_name'] == 'LE':
            category = 'LIMITED EDITION'
        elif self.kwargs['category_name'] == 'S':
            category = 'STATIONARIES'
        elif self.kwargs['category_name'] == 'F':
            category = 'FASHION'
        else:
            category = 'CROSSOVER'
        context['category'] = category
        return context
    

    # call products by 'object_list' in the template

class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"

class ProductCreateView(CreateView):
    form_class = ProductModalForm
    template_name ="products/product_create.html"
    queryset = Product.objects.all()
    
    def form_valid(self, form):
        product = form.save(commit=False)
        product.uploader = Profile.objects.get(user=self.request.user)
        product.save()
        return super().form_valid(form)

class ProductCartView(DetailView):
    model = Product
    template_name = "products/product_cart.html"

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductModalForm
    template_name = "products/product_update.html"

    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_object(self):
        _id = self.kwargs.get('pk')
        return get_object_or_404(Product, pk=_id)

def delete_product(request, pk):
    product = Product.objects.get(pk=pk)
    product.delete()
    return redirect('webb:admin')

def see_creator_product_detail(request):
    product_id = request.GET.get('product_id')
    product = Product.objects.get(pk=product_id)
    return render(request, 'creator/creator_info_product_detail.html', {'product': product})

def generate_referenece_code():
    """Generate a reference code."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

@login_required
def add_to_cart(request, pk):
    product = Product.objects.get(pk=pk)
    quantity = int(request.GET.get('quantity'))
    profile = Profile.objects.get(user=request.user)
    order_product, created = OrderProduct.objects.get_or_create(user=profile, product=product, ordered=False, quantity=quantity)
    try:
        ## order exists
        order = Order.objects.get(user=profile, ordered=False)
        if order.products_set.filter(product=product).exists():
            ## order product already in cart
            order_product.quantity += quantity
            order_product.save()
        else:
            ## add a new order product in cart
            order.products.add(order_product)
        return redirect('webb:product_cart')
    except Order.DoesNotExist:
        ## no active order yet
        order = Order.objects.create(user=profile, reference_no=generate_referenece_code())
        order.products.add(order_product)
        return redirect('webb:product_cart')

@login_required
def remove_from_cart(request, pk):
    product = Product.objects.get(pk=pk)
    profile = Profile.objects.get(user=request.user)
    try:
        ## order exists
        order = Order.objects.get(user=profile, ordered=False)
        if order.products_set.filter(product=product).exists():
            ## order product in cart
            order_product = OrderProduct.objects.get(user=profile, product=product, ordered=False)
            order.products.remove(order_product)
            order_product.delete()
            return redirect('webb:product_cart')
        else:
            ## order product not in cart
            return redirect('webb:product_cart')
    except Order.DoesNotExist:
        return redirect('webb:product_cart')

@login_required
def change_order_product_quantity(request, pk, quanity):
    if int(quantity) == 0:
        remove_from_cart(pk=pk)
        return redirect('webb:product_cart')
    else:
        product = Product.objects.get(pk=pk)
        profile = Profile.objects.get(user=request.user)
        try:
            ## order exists
            order = Order.objects.get(user=profile, ordered=False)
            if order.products_set.filter(product=product).exists():
                ## order product in cart
                order_product = OrderProduct.objects.get(user=profile, product=product, ordered=False)
                order_product.quantity = quantity
                order_product.save()
                return redirect('webb:product_cart')
            else:
                ## order product not in cart
                return redirect('webb:product_cart')
        except Order.DoesNotExist:
            return redirect('webb:product_cart')    


## CREATOR ##
class CreatorDetailView(DetailView):
    model = Creator
    template_name = "creator/creator_info.html"
    # call creator by 'object' in the template 

class CreatorUpdateView(UpdateView):
    model = Creator
    form_class = CreatorModalForm
    template_name = 'creator/creator_update.html'

    def form_valid(self, form):
        creator = form.save()
        add_social_media_urls(self.request, creator.pk)
        return super().form_valid(form)

class CreatorCreateView(CreateView):
    model = Creator
    form_class = CreatorModalForm
    template_name = "creator/creator_create.html"

    def form_valid(self, form):
        creator = form.save(commit=False)
        creator.name = self.request.user.username
        creator.profile = Profile.objects.get(user=self.request.user)
        creator.save()
        add_social_media_urls(self.request, creator.pk)
        return super().form_valid(form)

def delete_creator(request, pk):
    creator = Creator.objects.get(pk=pk)
    creator.delete()
    return redirect('webb:home')

## BLOG ##  
class BlogListView(ListView):
    model = Blog
    paginate_by = 25

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogs/blog_article.html'

class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogModalForm
    template_name = 'blogs/blog_create.html'
    hashtag_set = Hashtag.objects.all()

    def form_valid(self, form):
        blog = form.save(commit=False)
        blog.user = Profile.objects.get(user=self.request.user)
        blog.save()
        add_blog_hashtags(self.request.POST.get('hashtag_ids'), blog.pk)
        return super().form_valid(form)

def add_blog_hashtags(hashtag_ids, pk):
    blog_id = pk
    blog = Blog.objects.get(pk=blog_id)
    h_ids = hashtag_ids.split(", ")
    h_ids.pop()
    for h_id in h_ids:
        hashtag = Hashtag.objects.get(pk=h_id)
        blog.hashtags.add(hashtag)
    return reverse('webb:blog_detail', kwargs={"pk": pk})
        
class BlogUpdateView(UpdateView):
    model = Blog
    form_class = BlogModalForm
    template_name = 'blogs/blog_update.html'

    def form_valid(self, form):
        blog = form.save(commit=False)
        blog.hashtags.clear()
        blog.save()
        add_blog_hashtags(self.request.POST.get('hashtag_ids'), blog.pk)
        return super().form_valid(form)

def blog_delete(request, pk):
    profile = Profile.objects.get(user=request.user)
    creator = Creator.objects.get(profile=profile)
    blog = Blog.objects.get(pk=pk)
    blog.delete()
    return HttpResponseRedirect(reverse('webb:creator_update', kwargs={"pk": int(creator.pk)}))

## Critique ##
class CritiqueListView(ListView):
    model = Critique
    paginate_by = 25

class CritiqueDetailView(DetailView):
    model = Critique
    template_name = 'critiques/critique_article.html'

class CritiqueCreateView(CreateView):
    model = Critique
    form_class = CritiqueModalForm
    template_name = 'critiques/critique_create.html'

    def form_valid(self, form):
        print('reached_here')
        critique = form.save(commit=False)
        critique.user = Profile.objects.get(user=self.request.user)
        critique.save()
        add_critique_hashtags(self.request.POST.get('hashtag_ids'), critique.pk)
        return super().form_valid(form)

def add_critique_hashtags(hashtag_ids, pk):
    critique_id = pk
    critique = Critique.objects.get(pk=critique_id)
    h_ids = hashtag_ids.split(", ")
    h_ids.pop()
    for h_id in h_ids:
        hashtag = Hashtag.objects.get(pk=h_id)
        critique.hashtags.add(hashtag)
    return reverse('webb:critique_detail', kwargs={"pk": pk})

class CritiqueUpdateView(UpdateView):
    model = Critique
    form_class = CritiqueModalForm
    template_name = 'critiques/critique_update.html'

    def form_valid(self, form):
        critique = form.save(commit=False)
        critique.hashtags.clear()
        critique.save()
        add_critique_hashtags(self.request.POST.get('hashtag_ids'), critique.pk)
        return super().form_valid(form)

def critique_delete(request, pk):
    profile = Profile.objects.get(user=request.user)
    creator = Creator.objects.get(profile=profile)
    critique = Critique.objects.get(pk=pk)
    critique.delete()
    return HttpResponseRedirect(reverse('webb:creator_update', kwargs={"pk": int(creator.pk)}))


## CREDENTIAL MANAGEMENT ##
def sign_up(request):
    if request.method == "POST":
        sign_up_form = SignUpForm(request.POST)
        if sign_up_form.is_valid():
            user = sign_up_form.save()
            profile = Profile(user=user)
            profile.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("webb:home")
    else:
        sign_up_form = SignUpForm()
        return render(request, "sign_up.html", {'form': sign_up_form })

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("webb:home")
        else:
            messages.warning(request, 'Please login again. The credentials you entered previously is not valid.')
    else:
        return redirect('webb:home')

def signout(request):
    logout(request)

        
### Hashtags ###
def create_hashtag(request):
    text = request.GET.get('text')
    text = text.lower()
    try:
        hashtag = Hashtag.objects.get(tag_text=text)
    except Hashtag.DoesNotExist:
        hashtag = Hashtag(tag_text=text)
        hashtag.save()
    hashtag_id = str(hashtag.pk)
    return JsonResponse({'hashtag_id': hashtag_id})

def delete_hashtag(request):
    blog_id = request.GET.get('blog_id')
    hashtag_id = request.GET.get('hashtag_id')
    blog = Blog.objects.get(pk=blog_id)
    hashtag = Hashtag.objects.get(pk=hashtag_id)
    blog.hashtags.remove(hashtag)
    return HttpResponseRedirect(reverse('webb:blog_update', kwargs={"pk": int(blog_id)}))

def delete_critique_hashtag(request):
    critique_id = request.GET.get('critique_id')
    hashtag_id = request.GET.get('hashtag_id')
    critique = Critique.objects.get(pk=critique_id)
    hashtag = Hashtag.objects.get(pk=hashtag_id)
    critique.hashtags.remove(hashtag)
    return HttpResponseRedirect(reverse('webb:critique_update', kwargs={"pk": int(critique_id)}))

class HashtagDetailView(DetailView):
    model = Hashtag
    template_name = 'hashtags/hashtag_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hashtags_list'] = Hashtag.objects.exclude(pk=self.get_object().pk).order_by('tag_text')
        return context

## Social Media Url ##
def add_social_media_urls(request, creator_pk):
    creator = Creator.objects.get(pk=creator_pk)
    ## instagram
    instagram_url = request.POST.get('instagram_url')
    create_social_media_url(creator, 'instagram', instagram_url)
    ## facebook
    facebook_url = request.POST.get('facebook_url')
    create_social_media_url(creator, 'facebook', facebook_url)
    ## pininterest
    pininterest_url = request.POST.get('pininterest_url')
    create_social_media_url(creator, 'pininterest', pininterest_url)
    ## twitter
    twitter_url = request.POST.get('twitter_url')
    create_social_media_url(creator, 'twitter', twitter_url)

def create_social_media_url(creator, brand, url):
    if url != "" and url != "NA":
        obj = SocialMediaUrl(profile=creator, brand=brand, url=url)
        obj.save()


## Hide or Reveal From Profile ##
def hide_from_profile(request):
    type_obj = request.GET.get('object_type')
    obj = request.GET.get('object_pk')
    if type_obj == 'product':
        obj_instance = Product.objects.get(pk=obj)
    elif type_obj == 'blog':
        obj_instance = Blog.objects.get(pk=obj)
    else:
        obj_instance = Critique.objects.get(pk=obj)
    obj_instance.hide_from_profile = not obj_instance.hide_from_profile
    obj_instance.save()
    print(obj_instance.hide_from_profile)
    return HttpResponse('success')

# following and unfollowing -- BOTH AJAX
def follow(request):
    follower = Profile.objects.get(pk=request.GET.get('self_pk'))
    following = Profile.objects.get(pk=request.GET.get('creator_pk'))
    following_relationship = ProfileFollowing(follower=follower, following=following)
    following_relationship.save()
    return HttpResponse('success')

def unfollow(request):
    follower = Profile.objects.get(pk=request.GET.get('self_pk'))
    following = Profile.objects.get(pk=request.GET.get('creator_pk'))
    try:
        relationship = ProfileFollowing.objects.get(follower=follower, following=following)
        relationship.delete()
    except ProfileFollowing.DoesNotExist:
        print("This relationship does not exist")
    except Employee.MultipleObjectsReturned:
        print("System shows that this follower has followed this creator for more than once.")
    return HttpResponse('unfollow')

## Address
def load_address_form(request):
    form = AddressModalForm
    return render(request, 'address/address_form.html', {'form': form})

def create_address(request):
    profile = Profile.objects.get(user=request.user)
    country = request.GET.get('country')
    city = request.GET.get('city')
    zip_code = request.GET.get('zip_code')
    address = request.GET.get('address')
    address_2 = request.GET.get('address_2')
    type_a = request.GET.get('type')
    address = Address(country=country, city=city, zip_code=zip_code, address=address, 
    address_types=type_a, address_2=address_2, user=profile)
    address.save()
    return HttpResponse(str(address))

def update_address_modal(request, pk):
    address = Address.objects.get(pk=pk)
    return render(request, 'address/address_update.html', {'address': address, 'form': AddressModalForm})

def update_address(request, pk):
    address = Address.objects.get(pk=pk)
    address.country = request.GET.get('country')
    address.city = request.GET.get('city')
    address.zip_code = request.GET.get('zip_code')
    address.address = request.GET.get('address')
    address.address_2 = request.GET.get('address_2')
    address.save()
    return HttpResponse(str(address))

## Order

class OrderDetailView(DetailView):
    model = Order
    template_name = 'order/order_detail.html'

## TODO: render active order to the modal
def order_cart_view(request):
    profile = Profile.objects.get(user=request.user)
    try:
        order = Order.objects.get(user=profile, ordered=False)
        return render(request, 'order/active_order.html', {'order': order})
    except:
        return render(request, 'order/active_order.html', {})

## EMAIL
## TODO: send verification email function to be implemented
def send_verification_email(request):
    pass

def verify_email(request):
    try:  
        user_id = force_text(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(id=user_id)  
        profile = user.profile
    except(TypeError, ValueError, OverflowError, User.DoesNotExist, Profile.DoesNotExist):  
        user = None 
        profile = None
    if user is not None and profile is not None and email_verification_token.check_token(user, token):  
        user.is_active = True 
        profile.email_verified = True 
        user.save()  
        profile.save()
        return render(request, 'verification_email/email_verified.html', {'user': user})
    else:  
        return HttpResponse('Activation link is invalid!')

## TODO: send order confirm email function to be implemented
## need to past in order and user
def send_order_confirm_email(request):
    pass


## CHECKOUT FORM 
def checkout_form(request, pk):
    order = Order.objects.get(pk=pk)
    user = request.user
    profile = Profile.objects.get(user=user)
    shipping_address = profile.get_shipping_address()
    billing_address = profile.get_billing_address()
    if shipping_address is not None and billing_address is not None:
        context = {
            'shipping_address': shipping_address.address,
            'shipping_address2': shipping_address.address_2,
            'shipping_city': shipping_address.city,
            'shipping_country': shipping_address.country,
            'billing_address': billing_address.address,
            'billing_address2': billing_address.address_2,
            'billing_city': billing_address.city,
            'billing_country': billing_address.country
        }
    else:
        context = {}
    return render(request, 'checkout.html', {'form': CheckoutForm(initial=context), 'order': order})



## REST FRAMEWORKS VIEW ##
class ApiProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all() 

class ApiUserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class ApiProfileView(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

class ApiCreatorView(viewsets.ModelViewSet):
    serializer_class = CreatorSerializer
    queryset = Creator.objects.all()

class ApiAddressView(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

class ApiCategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

# class ApiPaymentView(viewsets.ModelViewSet):
#     serializer_class = PaymentSerializer
#     queryset = Payment.objects.all()

class ApiOrderView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

class ApiOrderProductView(viewsets.ModelViewSet):
    serializer_class = OrderProductSerializer
    queryset = OrderProduct.objects.all()

class ApiBlogView(viewsets.ModelViewSet):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()

class ApiCritiqueView(viewsets.ModelViewSet):
    serializer_class = CritiqueSerializer
    queryset = Critique.objects.all()

class ApiReportView(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()







    