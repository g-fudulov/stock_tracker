from django.urls import path
from stock_portfolio_tracker.stock_tracker_users import views

urlpatterns = [
    path('', views.Homepage.as_view(), name='homepage'),
    path("login/", views.LoginUser.as_view(), name='login_user'),
    path("logout/", views.LogoutUser.as_view(), name='logout_user'),
    path("register/", views.RegisterUser.as_view(), name='register_user'),

]
