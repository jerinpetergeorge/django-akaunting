from django.urls import path

from .views import AboutPageView, DashBoardPageView, HomePageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("dash/", DashBoardPageView.as_view(), name="dashboard"),
    path("about/", AboutPageView.as_view(), name="about"),
]
