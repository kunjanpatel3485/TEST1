from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Watchlist
from .models import (
    User, BeginnerInvestor, IntermediateInvestor, FinancialAdvisor,
    Admin, Stock, Portfolio, MarketTrend, RecommendationEngine
)

# User Registration Form
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'accountBalance']

    #  def clean_accountBalance(self):
    #     accountBalance = self.cleaned_data.get('accountBalance')
    #     if accountBalance < 0:
    #         raise ValidationError("Account balance cannot be negative.")
    #     return accountBalance

# Custom User Creation Form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2', 'accountBalance']

# Beginner Investor Form
class BeginnerInvestorForm(forms.ModelForm):
    class Meta:
        model = BeginnerInvestor
        fields = ['experienceLevel', 'preferredInvestmentType', 'riskTolerance']

# Intermediate Investor Form
class IntermediateInvestorForm(forms.ModelForm):
    class Meta:
        model = IntermediateInvestor
        fields = ['experienceLevel', 'portfolioSize', 'tradingStrategy']

# Financial Advisor Form
class FinancialAdvisorForm(forms.ModelForm):
    clientList = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = FinancialAdvisor
        fields = ['certification', 'clientList', 'yearsOfExperience']

# Admin Form
class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['privileges']

# Stock Form
class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['symbol', 'companyName', 'currentPrice', 'peRatio', 'pbRatio', 'dividendYield']

# Portfolio Form
class PortfolioForm(forms.ModelForm):
    stocks = forms.ModelMultipleChoiceField(
        queryset=Stock.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Portfolio
        fields = ['user', 'stocks', 'riskLevel', 'totalInvestment']

# Market Trend Form
class MarketTrendForm(forms.ModelForm):
    class Meta:
        model = MarketTrend
        fields = ['indexName', 'trendData', 'marketVolatility']

# Recommendation Engine Form
class RecommendationEngineForm(forms.ModelForm):
    recommendedStocks = forms.ModelMultipleChoiceField(
        queryset=Stock.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = RecommendationEngine
        fields = ['user', 'recommendedStocks', 'recommendationCriteria']

class WatchlistForm(forms.ModelForm):
    class Meta:
        model = Watchlist
        fields = ['stock']