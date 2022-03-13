from django.urls import path

from .views import AboutPageView, DashboardPageView, HomePageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("dash/", DashboardPageView.as_view(), name="dashboard"),
    path("about/", AboutPageView.as_view(), name="about"),
]
