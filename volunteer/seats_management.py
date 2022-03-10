import itertools

from refugee.models import TransferServiceReservation
from volunteer.models import Transfer


class SeatsManagement:
    def __init__(self, transfer: Transfer):
        self.transfer = transfer
        self.total_seats = transfer.total_seats
        self.cities = [(i.city.id, i.route_order, str(i.city)) for i in transfer.stopovers]

    def _replace_order_by_city_id(self, available_seats: dict):
        city_order = {i[1]: i[0] for i in self.cities}
        return {(city_order[k[0]], city_order[k[1]]): v for k, v in available_seats.items()}

    def _replace_order_by_city_name(self, available_seats: dict):
        city_order = {i[1]: i[2] for i in self.cities}
        return {(city_order[k[0]], city_order[k[1]]): v for k, v in available_seats.items()}

    def cities_order(self):
        return {i[0]: i[1] for i in self.cities}

    def determine_available_seats(self, return_by_name=False) -> dict:
        route_orders = [i[1] for i in self.cities]  # already sorted in ascending order by sql
        cities_order = self.cities_order()

        available_seats = {}
        booked_seats = {
            (cities_order[i.start_city.id], cities_order[i.end_city.id]): i.seats
            for i in TransferServiceReservation.objects.filter(transfer=self.transfer).select_related(
                "start_city", "end_city"
            )
        }

        # tuples of (start_city_order,end_city_order)
        route_possibilities = list(itertools.combinations(route_orders, 2))

        for start_city_order, end_city_order in route_possibilities:
            available_seats[(start_city_order, end_city_order)] = self.total_seats
            for i, j in route_possibilities:
                if j <= start_city_order or i >= end_city_order:
                    continue
                available_seats[(start_city_order, end_city_order)] -= booked_seats.get((i, j), 0)

        return (
            self._replace_order_by_city_id(available_seats)
            if not return_by_name
            else self._replace_order_by_city_name(available_seats)
        )