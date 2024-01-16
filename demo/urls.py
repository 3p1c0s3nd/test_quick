"""
URL configuration for demo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from core.views import ClientListView, ProductListView, BillListView, UserRegistrationView, UserLoginView, download_clients_csv, upload_clients_csv


urlpatterns = [
    #path('admin/', admin.site.urls),
    path('clients/', ClientListView.as_view(), name='client-list'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('bills/', BillListView.as_view(), name='bill-list'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('download-clients-csv/', download_clients_csv, name='download-clients-csv'),
    path('upload-clients-csv/', upload_clients_csv, name='upload-clients-csv'),

]
