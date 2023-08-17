from django.forms import ModelForm
from . import models


class AuctionForm(ModelForm):
    class Meta:
        model = models.Auction
        fields = [
            'name',
            'time_transportation',
            'start_address',
            'finish_address',
            'length',
            'min_price',
            'max_price',
            'interval',
            'step',
            'more_info',
        ]


class CarrierFormForUser(ModelForm):
    class Meta:
        model = models.Carrier
        fields = [
            'name',
            'contact_info',
        ]


class CarrierFormForAdmin(ModelForm):
    class Meta:
        model = models.Carrier
        fields = [
            'name',
            'contact_info',
            'in_black_list',
        ]
