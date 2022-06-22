from django.urls import reverse
from django.views.generic.edit import FormView

from .forms import PaymentUpdateFom


class PaymentBulkUpdateView(FormView):
    template_name = "payments/admin/payment-bulk-update.html"
    form_class = PaymentUpdateFom

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["pks"] = self.request.GET.get("pks")
        return kwargs

    def get_success_url(self):
        return self.request.GET.get("from", reverse("admin:index"))
