from django.contrib import admin
from django.urls import path, include, re_path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('account.urls')),
    path('', views.home, name="home"),
    path('profile/', views.profile, name="profile"),
    path('purchase/<int:id>', views.purchase, name="purchase"),
    path('verify/', views.verify, name="verify"),
    path('cancel/<int:id>', views.cancel_ticket, name="cancel_ticket"),
    path('contact/', views.contact, name="contact"),

    re_path('.*', views.error_page),
]
