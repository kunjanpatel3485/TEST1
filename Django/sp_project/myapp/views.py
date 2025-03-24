import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import User, Stock, Watchlist
from .forms import UserForm, WatchlistForm
from .forms import FeedbackForm

# List of Nifty 50 & Sensex stocks
NIFTY_SENSEX_STOCKS = [
    {"companyName": "Reliance Industries", "symbol": "RELIANCE", "currentPrice": 2400},
    {"companyName": "Tata Consultancy Services", "symbol": "TCS", "currentPrice": 3800},
    {"companyName": "HDFC Bank", "symbol": "HDFCBANK", "currentPrice": 1600},
    {"companyName": "Infosys", "symbol": "INFY", "currentPrice": 1700},
    {"companyName": "ICICI Bank", "symbol": "ICICIBANK", "currentPrice": 930},
    {"companyName": "Hindustan Unilever", "symbol": "HINDUNILVR", "currentPrice": 2500},
    {"companyName": "State Bank of India", "symbol": "SBIN", "currentPrice": 600},
    {"companyName": "Kotak Mahindra Bank", "symbol": "KOTAKBANK", "currentPrice": 1700},
    {"companyName": "Bharti Airtel", "symbol": "BHARTIARTL", "currentPrice": 950},
    {"companyName": "ITC", "symbol": "ITC", "currentPrice": 450},
    {"companyName": "Larsen & Toubro", "symbol": "LT", "currentPrice": 2700},
    {"companyName": "Axis Bank", "symbol": "AXISBANK", "currentPrice": 950},
    {"companyName": "Bajaj Finance", "symbol": "BAJFINANCE", "currentPrice": 6500},
    {"companyName": "Asian Paints", "symbol": "ASIANPAINT", "currentPrice": 2900},
    {"companyName": "Maruti Suzuki", "symbol": "MARUTI", "currentPrice": 9000},
    {"companyName": "HCL Technologies", "symbol": "HCLTECH", "currentPrice": 1300},
    {"companyName": "Wipro", "symbol": "WIPRO", "currentPrice": 500},
    {"companyName": "Titan Company", "symbol": "TITAN", "currentPrice": 3200},
    {"companyName": "Sun Pharma", "symbol": "SUNPHARMA", "currentPrice": 1250},
    {"companyName": "UltraTech Cement", "symbol": "ULTRACEMCO", "currentPrice": 8700},
    {"companyName": "Nestle India", "symbol": "NESTLEIND", "currentPrice": 22000},
    {"companyName": "Tech Mahindra", "symbol": "TECHM", "currentPrice": 1200},
    {"companyName": "Mahindra & Mahindra", "symbol": "M&M", "currentPrice": 1600},
    {"companyName": "IndusInd Bank", "symbol": "INDUSINDBK", "currentPrice": 1400},
    {"companyName": "Power Grid Corporation", "symbol": "POWERGRID", "currentPrice": 250},
    {"companyName": "Tata Motors", "symbol": "TATAMOTORS", "currentPrice": 800},
    {"companyName": "Bajaj Finserv", "symbol": "BAJAJFINSV", "currentPrice": 1800},
    {"companyName": "HDFC Life", "symbol": "HDFCLIFE", "currentPrice": 580},
    {"companyName": "Grasim Industries", "symbol": "GRASIM", "currentPrice": 1800},
    {"companyName": "JSW Steel", "symbol": "JSWSTEEL", "currentPrice": 780},
    {"companyName": "Oil and Natural Gas Corporation", "symbol": "ONGC", "currentPrice": 210},
    {"companyName": "TATA", "symbol": "TATA POWER", "currentPrice": 357}
]

def add_nifty_sensex_stocks():
    """ Adds Nifty 50 & Sensex stocks to the database if missing """
    # Remove Tesla stock if it exists
    Stock.objects.filter(symbol="TSLA").delete()

    for stock in NIFTY_SENSEX_STOCKS:
        Stock.objects.update_or_create(
            symbol=stock["symbol"],
            defaults={
                "companyName": stock["companyName"],
                "currentPrice": stock["currentPrice"]
            },
        )

def company_view(request):
    """ Fetch and display only Nifty 50 & Sensex stocks """
    add_nifty_sensex_stocks()  # Ensure all stocks are in the database
    companies = Stock.objects.filter(symbol__in=[stock["symbol"] for stock in NIFTY_SENSEX_STOCKS])
    return render(request, "company.html", {"companies": companies})


def watchlist_view(request):
    watchlist = Watchlist.objects.filter(user=request.user)
    return render(request, "watchlist.html", {"watchlist": watchlist})


def add_to_watchlist(request, stock_id):
    stock = get_object_or_404(Stock, stockID=stock_id)
    watchlist_item, created = Watchlist.objects.get_or_create(user=request.user, stock=stock)
    
    if created:
        messages.success(request, f"{stock.companyName} added to your Watchlist!")
    else:
        messages.info(request, f"{stock.companyName} is already in your Watchlist.")
    
    return redirect("company")

def remove_from_watchlist(request, stock_id):
    if request.method == "POST":
        Watchlist.objects.filter(user=request.user, stock_id=stock_id).delete()
        messages.success(request, "Stock removed from your Watchlist.")
    return redirect("watchlist")

# def add_to_watchlist(request, stock_id):
#     stock = get_object_or_404(Stock, stockID=stock_id)
#     watchlist_item, created = Watchlist.objects.get_or_create(user=request.user, stock=stock)

#     if created:
#         messages.success(request, f"{stock.companyName} added to your Watchlist!")
#     else:
#         messages.info(request, f"{stock.companyName} is already in your Watchlist.")

#     return redirect("company")

# @login_required
# def watchlist_view(request):
#     watchlist = Watchlist.objects.filter(user=request.user)
#     return render(request, "watchlist.html", {"watchlist": watchlist})

# def stock_news(request):
#     api_key = "IFG6U8WK4NJ9TTHX"  
#     url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey={api_key}"

#     response = requests.get(url)
#     data = response.json()
#     articles = data.get("feed", []) 

#     return render(request, "news.html", {"articles": articles})

def signup_view(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])  
            user.save()  
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
        else: 
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = UserForm()
    
    return render(request, "signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")  
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def home_view(request):
    return render(request, "home.html")

def nifty_view(request):
    return render(request, "nifty.html")

def news_view(request):
    return render(request, "news.html")


def about_view(request):
    return render(request, "about.html")

def portfolio_view(request):
    return render(request, "portfolio.html")


def feedback_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)  
        if form.is_valid():
            form.save()  
            messages.success(request, "Your message has been sent successfully!")
            return redirect("feedback")  
    else:
        form = FeedbackForm() 
    
    return render(request, "feedback.html", {"form": form})