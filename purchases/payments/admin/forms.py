import typing

from django import forms

from ..models import Payment


class PaymentUpdateFom(forms.ModelForm):
    def __init__(self, *args, pks: typing.Optional[str] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["vendor"].required = False
        self.fields["category"].required = False
        if pks is not None:
            pks = [pk for pk in pks.split(",")]
        self.pks = pks

    class Meta:
        model = Payment
        fields = ["vendor", "category"]

    def save(self, commit=True):
        qs = Payment.objects.filter(pk__in=self.pks)
        if self.cleaned_data["vendor"]:
            qs.update(vendor=self.cleaned_data["vendor"])

        if self.cleaned_data["category"]:
            qs.update(vendor=self.cleaned_data["category"])
