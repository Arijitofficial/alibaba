from django.urls import path
from . import views


urlpatterns=[
            path('',views.home),
            path('signupin',views.signupin),
            path('sig',views.sig),
            path('log_in',views.log_in),
            path('forgot_password',views.fopd),
            path('fpd',views.fpd),
            path('detail/<int:id>', views.detail),
            path('add_to_cart/<str:id>',views.add_to_cart),
            path('cart',views.open_cart),
            ]