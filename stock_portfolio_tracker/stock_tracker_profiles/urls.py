from django.urls import path
from stock_portfolio_tracker.stock_tracker_profiles import views

urlpatterns = [
    path('details/<int:profile_pk>/', views.ProfileDetails.as_view(), name='profile_details'),
    path('update/<int:profile_pk>/', views.UpdateDetails.as_view(), name='profile_update')
]
