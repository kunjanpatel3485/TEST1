import requests
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from .models import User  
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Stock, Watchlist
from .forms import WatchlistForm
from django.contrib import messages



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


def home_view(request):
    return render(request, "home.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def company_view(request):
    return render(request, "company.html")

def nifty_view(request):
    return render(request, "nifty.html")

def news_view(request):
    return render(request, "news.html")


def company_view(request):
    companies = Stock.objects.all()
    print(companies)  
    return render(request, "company.html", {"companies": companies})

def add_to_watchlist(request, stock_id):
    stock = get_object_or_404(Stock, stockID=stock_id)  # Use stockID

    watchlist_item, created = Watchlist.objects.get_or_create(user=request.user, stock=stock)

    if created:
        messages.success(request, f"{stock.companyName} added to your Watchlist!")
    else:
        messages.info(request, f"{stock.companyName} is already in your Watchlist.")

    return redirect('company')


def watchlist_view(request):
    watchlist = Watchlist.objects.filter(user=request.user)
    return render(request, "watchlist.html", {"watchlist": watchlist})

def stock_news(request):
    api_key = "IFG6U8WK4NJ9TTHX"  
    url = "https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey=" + api_key

    response = requests.get(url)
    data = response.json()

    articles = data.get("feed", []) 

    return render(request, "news.html", {"articles": articles})



# def toggle_watchlist(request, company_id):
#     company = get_object_or_404(Company, id=company_id)
#     watchlist_item, created = Watchlist.objects.get_or_create(user=request.user, company=company)

#     if not created:
#         watchlist_item.delete()
#         return JsonResponse({'status': 'removed'})

#     return JsonResponse({'status': 'added'})

# def watchlist_view(request):
#     watchlist_items = Watchlist.objects.filter(user=request.user)
#     return render(request, "watchlist.html", {"watchlist_items": watchlist_items})