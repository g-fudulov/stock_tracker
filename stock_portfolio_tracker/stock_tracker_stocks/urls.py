from django.urls import path
from stock_portfolio_tracker.stock_tracker_stocks import views

urlpatterns = [
    path('details/<int:portfolio_pk>/', views.PortfolioDetails.as_view(), name='portfolio_details'),
    path('add-position/<int:portfolio_pk>/', views.add_stock_to_portfolio, name='add_stock'),
    path('buy/<int:portfolio_pk>/<str:stock_symbol>/', views.buy_stock, name='buy_stock'),
    path('sell/<int:portfolio_pk>/<str:stock_symbol>/', views.sell_stock, name='sell_stock'),
    path('remove/<int:portfolio_pk>/<str:stock_symbol>/', views.RemoveStock.as_view(), name='remove_stock'),
    path('sales/<int:profile_pk>/<int:portfolio_pk>/', views.SalesDetails.as_view(), name='sales_details'),
    path('buys/<int:profile_pk>/<int:portfolio_pk>/', views.BuysDetails.as_view(), name='buys_details'),
]
