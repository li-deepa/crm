from django.contrib.auth import views as auth_views
from django.urls import path
from .import views

urlpatterns = [
    path('', views.home,name='home'),
    
    path('login', views.loginPage,name='login'),
    path('register',views.registerPage,name='register'),
    path('logout', views.logoutUser,name='logout'),
   

    path('create_product', views.create_product,name='create_product'),
    path('update_product/<str:pk>/', views.update_product,name='update_product'),
    path('products', views.products,name='products'),
    path('customer_info',views.customer_info,name='customer_info'),
    path('customer/<str:pk_test>/',views.customer,name='customer'),

    path('create_order/<str:pk>/', views.createOrder,name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder,name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder,name='delete_order'),

    path('profile', views.profile,name='profile'),
    path('profile_settings', views.profile_settings,name='profile_settings'),

    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),name="password_reset_complete"),


]

# submit email form   password resetview
# email success sent message 
# link to password reset form in html
# password successfully changed message
