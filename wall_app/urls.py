from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('success', views.success),
    path('logout', views.logout),
    path('post_message', views.post_message),
    path('add_comment/<int:id>', views.add_comment),
    path('user_profile/<int:id>', views.profile),
    path('like/<int:id>', views.add_like),
]