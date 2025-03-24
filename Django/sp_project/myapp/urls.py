from django.urls import path
from . import views
from .views import company_view

# from .views import add_to_watchlist, watchlist_view


urlpatterns = [
    path('', views.home_view, name="home"),
    path('home/', views.home_view, name="home"),
    path('signup/', views.signup_view, name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('company/', company_view, name="company"),
    path('nifty/', views.nifty_view, name="nifty"),
    path('news/', views.news_view, name="news"),
    path('add_to_watchlist/<int:stock_id>/', views.add_to_watchlist, name="add_to_watchlist"),
    path('watchlist/remove/<int:stock_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),  # NEW ROUTE
    path('watchlist/', views.watchlist_view, name="watchlist"),
    # path("news/", views.stock_news, name="news"),
    path('about/',views.about_view, name="about"),
    path('feedback/',views.feedback_view, name="feedback"),
    path('portfolio/', views.portfolio_view, name="portfolio"),

]
