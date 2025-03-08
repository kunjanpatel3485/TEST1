from django.urls import path
from . import views
from .views import company_view

# from .views import add_to_watchlist, watchlist_view


urlpatterns = [
    path('', views.login_view, name="login"),
    path('home/', views.home_view, name="home"),
    path('signup/', views.signup_view, name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('company/', company_view, name="company"),
    path('nifty/', views.nifty_view, name="nifty"),
    path('news/', views.news_view, name="news"),
    path('add_to_watchlist/<int:stock_id>/', views.add_to_watchlist, name="add_to_watchlist"),
    path('watchlist/', views.watchlist_view, name="watchlist"),
    path("news/", views.stock_news, name="news"),

]
