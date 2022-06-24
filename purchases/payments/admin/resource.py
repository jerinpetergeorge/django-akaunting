from import_export import resources

from purchases.payments.models import Payment


class PaymentResource(resources.ModelResource):
    class Meta:
        model = Payment
        fields = (
            "id",
            "item",
            "amount",
            "date",
            "vendor",
            "category",
            "payment_method",
        )
        export_order = (
            "id",
            "date",
            "item",
            "amount",
            "category",
            "vendor",
            "payment_method",
        )
