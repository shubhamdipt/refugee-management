from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from organization.models import Transfer
from organization.seats_management import SeatsManagement
from refugee.models import TransferReservation


class TransferReservationForm(forms.Form):
    transfer_id = forms.IntegerField(widget=forms.HiddenInput())
    start_time = forms.CharField(label=_("Start time"))
    from_city = forms.ChoiceField(label=_("From"))
    to_city = forms.ChoiceField(label=_("To"))
    seats = forms.IntegerField(label=_("Number of seats"))

    def __init__(self, transfer, refugee, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stopovers_choices = [(i.city.id, str(i.city)) for i in transfer.stopovers]
        self.fields["from_city"].choices = stopovers_choices
        self.fields["to_city"].choices = stopovers_choices
        self.fields["transfer_id"].initial = transfer.id
        self.fields["start_time"].initial = transfer.start_time
        self.fields["start_time"].disabled = True
        self.refugee = refugee

    def clean(self):
        cleaned_data = super().clean()
        transfer = Transfer.objects.get(id=cleaned_data.get("transfer_id"))
        from_city = int(cleaned_data.get("from_city"))
        to_city = int(cleaned_data.get("to_city"))
        seats = int(cleaned_data.get("seats"))

        seat_management = SeatsManagement(transfer=transfer)

        cities_order = seat_management.cities_order()
        if from_city and to_city:
            # Only do something if both fields are valid so far.
            if from_city == to_city:
                raise ValidationError("From city and to city cannot be the same.")
            if cities_order[from_city] >= cities_order[to_city]:
                raise ValidationError("From city cannot be after to city in the route.")
        else:
            raise ValidationError("Both from city and to city are required.")

        seat_management = SeatsManagement(transfer=transfer)
        seats_available = seat_management.determine_available_seats().get((from_city, to_city))
        if seats < 1:
            raise ValidationError("At least one seat is required for a reservation.")
        if seats_available < seats:
            raise ValidationError(f"Only {seats_available} left for this trip.")

        if (
                TransferReservation.objects.filter(
                    refugee=self.refugee,
                    transfer__start_time__gt=timezone.now()
                ).count()
                > 0
        ):
            raise ValidationError("Multiple active reservations are not allowed.")
