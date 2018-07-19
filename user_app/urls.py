from django.urls import path, re_path

from user_app import views, verifycode

urlpatterns = [
	path('register/', views.register),
	path('login/', views.user_login),
	path('index/', views.index),
	path('logout/', views.user_logout),
	path('change_password/', views.apply_for_change_password),
	path('change_password_true/', views.change_password_true),
	re_path(r'^verify_code', verifycode.verify_code),

]