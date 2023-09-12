from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from stock_portfolio_tracker.stock_tracker_stocks.models import Portfolio, PortfolioItem, Stock
from django.views import generic as views
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from stock_portfolio_tracker.stock_tracker_stocks.forms import StockAddForm

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


@login_required(login_url=reverse_lazy('login_user'))
def add_stock_to_portfolio(request, portfolio_pk):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_pk)

    if request.user.pk != portfolio.owner.user.pk:  # Check for access
        return render(request, 'access_denied.html')

    form = StockAddForm()
    if request.method == 'POST':
        form = StockAddForm(request.POST)
        if form.is_valid():
            # Get or create the stock (based on symbol)
            symbol = form.cleaned_data['symbol']
            stock, created = Stock.objects.get_or_create(symbol=symbol, defaults={
                'name': form.cleaned_data['name'],
                'price': form.cleaned_data['price'],
            })
            """Creates a new PortfolioItem instance by the ticker symbol"""
            existing_portfolio_item = PortfolioItem.objects.filter(portfolio=portfolio, stock=stock).first()

            if existing_portfolio_item:
                total_quantity = existing_portfolio_item.quantity + form.cleaned_data['quantity']
                total_cost = ((existing_portfolio_item.quantity * existing_portfolio_item.average_purchase_price)
                              + (form.cleaned_data['quantity'] * form.cleaned_data['price']))
                average_purchase_price = total_cost / total_quantity

                existing_portfolio_item.quantity = total_quantity
                existing_portfolio_item.average_purchase_price = average_purchase_price
                existing_portfolio_item.save()
            else:
                # Create a new portfolio item with the specified stock and quantity
                PortfolioItem.objects.create(
                    portfolio=portfolio,
                    stock=stock,
                    quantity=form.cleaned_data['quantity'],
                    average_purchase_price=form.cleaned_data['price'],
                )

            return redirect('portfolio_details', portfolio_pk=portfolio_pk)

    return render(request, 'portfolio/add.html', {'form': form})
