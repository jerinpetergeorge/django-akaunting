from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"


class DashBoardPageView(LoginRequiredMixin, TemplateView):
    template_name = "pages/dash/dash.html"
