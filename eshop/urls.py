"""
URL configuration for eshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from front import views
from myauth import views as myauth_views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('admin/', include('admin_volt.urls')),
    path('', views.home, name='home'),
    path('details/<slug:prod_slug>', views.details, name='details'),
    path('shop', views.shop, name='shop'),
    path('shop/<slug:cat_slug>', views.shop, name='shop'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('contact', views.contact, name='contact'),
    # path('login', myauth_views.login, name='login'),
    path('login', 
         view=LoginView.as_view(template_name='myauth/login.html', next_page='home', redirect_authenticated_user=True),
         name='login'),
    path('logout', 
         view=LogoutView.as_view(),
         name='logout'),
    path('register', myauth_views.register, name='register'),
    path('forgot_password', myauth_views.forgot_password, name='forgot_password'),
    path('updatepassword/<str:token>/<str:uid>', myauth_views.update_password, name='update_password'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)