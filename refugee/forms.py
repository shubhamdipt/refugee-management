from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from refugee.models import TransferServiceReservation
from volunteer.models import Transfer
from volunteer.seats_management import SeatsManagement


class TransferServiceReservationForm(forms.Form):
    transfer_id = forms.IntegerField(widget=forms.HiddenInput())
    pick_up_time = forms.CharField(label=_("Pick up"))
    start_city = forms.ChoiceField(label=_("From"))
    end_city = forms.ChoiceField(label=_("To"))
    seats = forms.IntegerField(label=_("Number of seats"))

    def __init__(self, transfer, refugee, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stopovers_choices = [(i.city.id, str(i.city)) for i in transfer.stopovers]
        self.fields["start_city"].choices = stopovers_choices
        self.fields["end_city"].choices = stopovers_choices
        self.fields["transfer_id"].initial = transfer.id
        self.fields["pick_up_time"].initial = transfer.pick_up_time
        self.fields["pick_up_time"].disabled = True
        self.refugee = refugee

    def clean(self):
        cleaned_data = super().clean()
        transfer_instance = Transfer.objects.get(id=cleaned_data.get("transfer_id"))
        start_city = int(cleaned_data.get("start_city"))
        end_city = int(cleaned_data.get("end_city"))
        seats = int(cleaned_data.get("seats"))

        seat_management = SeatsManagement(transfer=transfer_instance)

        cities_order = seat_management.cities_order()
        if start_city and end_city:
            # Only do something if both fields are valid so far.
            if start_city == end_city:
                raise ValidationError("Start city and end city cannot be the same.")
            if cities_order[start_city] >= cities_order[end_city]:
                raise ValidationError("Start city cannot be after the end city in the route.")
        else:
            raise ValidationError("Both start city and end city are required.")

        seat_management = SeatsManagement(transfer=transfer_instance)
        seats_available = seat_management.determine_available_seats().get((start_city, end_city))
        if seats < 1:
            raise ValidationError("At least one seat is required for a reservation.")
        if seats_available < seats:
            raise ValidationError(f"Only {seats_available} left for this trip.")

        if TransferServiceReservation.objects.filter(transfer=transfer_instance, refugee=self.refugee).count() > 0:
            raise ValidationError("Multiple reservations for the same transfer is not allowed.")
