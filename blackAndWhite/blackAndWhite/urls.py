"""blackAndWhite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from webb.views import *
from rest_framework import routers  
from django.conf.urls.static import static 
from . import settings

router = routers.DefaultRouter() 
router.register(r'products', ApiProductView, 'products')
router.register(r'users', ApiUserView, 'users')
router.register(r'profiles', ApiProfileView, 'profiles')
router.register(r'creators', ApiCreatorView, 'creators')
router.register(r'addresses', ApiAddressView, 'addresses')
router.register(r'categories', ApiCategoryView, 'categories')
#router.register(r'payments', ApiPaymentView, 'payments')
router.register(r'orders', ApiOrderView, 'orders')
router.register(r'orderproducts', ApiOrderProductView, 'orderproducts')
router.register(r'blogs', ApiBlogView, 'blogs')
router.register(r'critiques', ApiCritiqueView, 'critiques')
router.register(r'reports', ApiReportView, 'reports') 

app_name = 'webb'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('webb/', include('webb.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/', include(router.urls)),
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
