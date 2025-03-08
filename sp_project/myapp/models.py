from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User



# Custom User Model
class User(AbstractUser):
    userID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    accountBalance = models.FloatField(default=0.0)

    def __str__(self):
        return self.username

# Beginner Investor Model
class BeginnerInvestor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experienceLevel = models.CharField(max_length=50)
    preferredInvestmentType = models.CharField(max_length=100)
    riskTolerance = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.name} (Beginner)"

# Intermediate Investor Model
class IntermediateInvestor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experienceLevel = models.CharField(max_length=50)
    portfolioSize = models.FloatField()
    tradingStrategy = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.name} (Intermediate)"

# Financial Advisor Model
class FinancialAdvisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    certification = models.CharField(max_length=255)
    clientList = models.ManyToManyField(User, related_name='advisor_clients', blank=True)
    yearsOfExperience = models.IntegerField()

    def __str__(self):
        return f"{self.user.name} (Advisor)"

# Admin Model
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    privileges = models.TextField()

    def __str__(self):
        return f"{self.user.name} (Admin)"

# Stock Model
class Stock(models.Model):
    stockID = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=10, unique=True)
    companyName = models.CharField(max_length=255)
    currentPrice = models.FloatField()
    peRatio = models.FloatField(null=True, blank=True)  # Allow NULL values
    pbRatio = models.FloatField(null=True, blank=True)
    dividendYield = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.symbol


    def setStockPrice(self, newPrice):
        self.currentPrice = newPrice
        self.save()

# Portfolio Model
class Portfolio(models.Model):
    portfolioID = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stocks = models.ManyToManyField(Stock, blank=True)
    riskLevel = models.CharField(max_length=50)
    totalInvestment = models.FloatField()

    def __str__(self):
        return f"{self.user.name}'s Portfolio"

# Market Trend Model
class MarketTrend(models.Model):
    trendID = models.AutoField(primary_key=True)
    indexName = models.CharField(max_length=255)
    trendData = models.JSONField()
    marketVolatility = models.FloatField()

    def __str__(self):
        return self.indexName

# Recommendation Engine Model
class RecommendationEngine(models.Model):
    recommendationID = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recommendedStocks = models.ManyToManyField(Stock, blank=True)
    recommendationCriteria = models.TextField()

    def __str__(self):
        return f"Recommendations for {self.user.name}"

User = get_user_model()

class Company(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)   # Default to stockID=1

    def __str__(self):
        return f"{self.user.username} - {self.stock.symbol}"
