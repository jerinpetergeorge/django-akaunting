from django.views.generic import TemplateView


class DashboardPageView(TemplateView):
    template_name = "pages/dashboard.html"


class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"
