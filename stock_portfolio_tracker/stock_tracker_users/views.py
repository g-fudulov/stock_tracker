from django.shortcuts import render
from django.views import generic as views
from stock_portfolio_tracker.stock_tracker_users import models
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from stock_portfolio_tracker.stock_tracker_stocks.models import Profile
from stock_portfolio_tracker.stock_tracker_stocks.models import Stock, PortfolioItem, Portfolio
from stock_portfolio_tracker.stock_tracker_users.forms import CustomRegisterUserForm

# Create your views here.
UserModel = get_user_model()


class Homepage(views.TemplateView):
    template_name = 'homepage.html'


class LoginUser(auth_views.LoginView):
    model = UserModel
    template_name = 'user/login.html'
    success_url = reverse_lazy('homepage')

    # TODO: return details portfolio
    # def get_success_url(self):
    #     return reverse_lazy()


class RegisterUser(views.CreateView):
    model = UserModel
    template_name = 'user/register.html'
    form_class = CustomRegisterUserForm
    success_url = reverse_lazy('homepage')

    # TODO: return details portfolio
    # def get_success_url(self):
    #     return reverse_lazy()

    def form_valid(self, form):
        response = super().form_valid(form)
        # Create a Profile instance for the newly registered user
        Profile.objects.create(user=self.object)
        login(self.request, self.object)
        return response


class LogoutUser(auth_views.LogoutView):
    # template_name = 'user/logout.html'
    pass



