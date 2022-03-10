from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from volunteer.models import TransferService


class TransferServiceReservationForm(forms.Form):
    transfer_id = forms.IntegerField(widget=forms.HiddenInput())
    pick_up_time = forms.CharField(label=_("Pick up"))
    start_city = forms.ChoiceField(label=_("Start city"))
    end_city = forms.ChoiceField(label=_("End city"))
    seats = forms.IntegerField(label=_("Number of seats"))

    def __init__(self, transfer_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if transfer_id:
            transfer_instance = TransferService.objects.get(id=transfer_id)
            stopovers_choices = [(i.city.id, str(i.city)) for i in transfer_instance.stopovers]
            self.fields["start_city"].choices = stopovers_choices
            self.fields["end_city"].choices = stopovers_choices
            self.fields["transfer_id"].initial = transfer_instance.id
            self.fields["pick_up_time"].initial = transfer_instance.pick_up_time
            self.fields["pick_up_time"].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        transfer_instance = TransferService.objects.get(id=cleaned_data.get("transfer_id"))
        start_city = int(cleaned_data.get("start_city"))
        end_city = int(cleaned_data.get("end_city"))

        transfer_cities_ids = {i.city.id: i.route_order for i in transfer_instance.stopovers}
        if start_city and end_city:
            # Only do something if both fields are valid so far.
            if start_city == end_city:
                raise ValidationError("Start city and end city cannot be the same.")
            if transfer_cities_ids[start_city] >= transfer_cities_ids[end_city]:
                raise ValidationError("Start city cannot be after the end city in the route.")
        else:
            raise ValidationError("Both start city and end city are required.")

        # TODO
        # if int(cleaned_data.get("seats")) >
