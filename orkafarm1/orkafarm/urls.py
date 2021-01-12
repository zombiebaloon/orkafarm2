"""orkafarm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from orka import views
from django.contrib import admin
from django.urls import path
from orka.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404, handler500
from django.views.static import serve
from django.conf.urls import url
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('about/', aboutus, name='about'),
    path('contact/', contact, name='contact'),
    # path('store/', store, name='store'),
    # path('cart/', cart, name='cart'),
    # path('checkout/', checkout, name='checkout'),
    # path('update_item/', updateItem, name='update_item'),
    # path('process_order/', processOrder, name='process_order'),
    path('Our-Farms/',farm, name='farm'),
    path('Terms-and-Conditions/',terms,name='terms'),
    path('Policy/',policy,name='policy'),
    path('Product(?P<int:id>)/',productView,name='productView'),
    # path('Login/',Login,name='Login'),
    path('OrderEnquiry/',bulkorders,name='bulkorder'),
    path('Madhu-D-Rajbhar/', madhu, name='madhu'),
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
    
]

urlpatterns += static(settings.MEDIA_URL,document_root =settings.MEDIA_ROOT)

handler404 = views.error_404
handler500 = views.error_500