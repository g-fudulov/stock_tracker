import requests
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from stock_portfolio_tracker.stock_tracker_stocks.models import Portfolio, PortfolioItem, Stock, Profile
from django.views import generic as views
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from stock_portfolio_tracker.stock_tracker_stocks.forms import BuyStockForm, SearchStockForm
import api_config

UserModel = get_user_model()


# Create your views here.

class PortfolioDetails(LoginRequiredMixin, UserPassesTestMixin, views.DetailView):
    model = Portfolio
    template_name = "portfolio/details.html"

    def get_object(self, queryset=None):
        pk = self.kwargs['portfolio_pk']
        return get_object_or_404(Portfolio, pk=pk)

    def test_func(self):
        return self.get_object().owner.user_id == self.request.user.pk

    def handle_no_permission(self):
        return render(self.request, 'access_denied.html', status=404)


def check_stock_exists(symbol):
    querystring = {"country": "United States", "symbol": f"{symbol}", "format": "json"}

    try:
        # Make a GET request to the API
        response = requests.get(api_config.url, headers=api_config.headers, params=querystring)

        if response.status_code == 200:
            # Parse the JSON response
            parsed_response = response.json()

            # Check if the response contains valid stock data
            if not parsed_response['data']:
                return False  # Does not exist
            else:
                return parsed_response  # Exists

        else:
            # Handle API request error (e.g., API key is invalid)
            return False

    except requests.exceptions.RequestException:
        # Handle network-related errors
        return False


@login_required(login_url=reverse_lazy('login_user'))
def add_stock_to_portfolio(request, portfolio_pk):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_pk)

    if request.user.pk != portfolio.owner.user.pk:  # Check for access
        return render(request, 'access_denied.html')

    form = SearchStockForm()
    if request.method == "POST":
        form = SearchStockForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['symbol']
            stock_data = check_stock_exists(symbol)

            if not stock_data:
                return render(request, 'portfolio/not_existing.html')

            parsed_symbol = stock_data['data'][0]['symbol']
            parsed_name = stock_data['data'][0]['name']
            stock, created = Stock.objects.get_or_create(
                symbol=parsed_symbol,
                defaults={
                    'name': parsed_name,
                    'price': 0,
                })

            existing_portfolio_item = PortfolioItem.objects.filter(portfolio=portfolio, stock=stock).first()

            if not existing_portfolio_item:
                PortfolioItem.objects.create(
                    portfolio=portfolio,
                    stock=stock,
                    quantity=0,
                    average_purchase_price=0,
                )

            return redirect('buy_stock', portfolio_pk=portfolio_pk, stock_symbol=parsed_symbol)

    return render(request, 'portfolio/search_stock.html', {"form": form})


@login_required(login_url=reverse_lazy('login_user'))
def buy_stock(request, portfolio_pk, stock_symbol):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_pk)
    stock = get_object_or_404(Stock, symbol=stock_symbol)
    portfolio_item = PortfolioItem.objects.filter(portfolio=portfolio, stock=stock).first()

    if request.user.pk != portfolio.owner.user.pk:  # Check for access
        return render(request, 'access_denied.html')

    form = BuyStockForm()
    if request.method == "POST":
        form = BuyStockForm(request.POST)
        if form.is_valid():
            """Calculate the average price per share"""
            total_quantity = portfolio_item.quantity + form.cleaned_data['quantity']
            total_cost = ((portfolio_item.quantity * portfolio_item.average_purchase_price)
                          + (form.cleaned_data['quantity'] * form.cleaned_data['price']))
            average_purchase_price = total_cost / total_quantity
            portfolio_item.average_purchase_price = average_purchase_price
            portfolio_item.quantity = total_quantity
            portfolio_item.save()

            return redirect('portfolio_details', portfolio_pk=portfolio_pk)

    return render(request, "portfolio/buy.html", {"form": form, 'portfolio_item': portfolio_item})


class RemoveStock(LoginRequiredMixin, UserPassesTestMixin, views.DeleteView):
    template_name = "portfolio/remove.html"

    def get_success_url(self):
        return reverse_lazy("portfolio_details", kwargs={"portfolio_pk": self.kwargs['portfolio_pk']})

    def get_object(self, queryset=None):
        portfolio_pk = self.kwargs['portfolio_pk']
        stock_symbol = self.kwargs['stock_symbol']
        stock = get_object_or_404(Stock, symbol=stock_symbol)
        return get_object_or_404(PortfolioItem, portfolio__id=portfolio_pk, stock=stock)

    def get_profile_of_portfolio(self):
        portfolio_pk = self.kwargs['portfolio_pk']
        portfolio = get_object_or_404(Portfolio, pk=portfolio_pk)
        return get_object_or_404(Profile, portfolio=portfolio)

    def test_func(self):
        return self.request.user.pk == self.get_profile_of_portfolio().user_id

    def handle_no_permission(self):
        return render(self.request, 'access_denied.html', status=404)