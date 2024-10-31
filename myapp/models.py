from django.db import models

class FlightBooking(models.Model):
    trip_type = models.CharField(max_length=10, choices=[('roundTrip', 'Round Trip'), ('oneWay', 'One Way')])
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    departure_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)  # Optional for one-way trips
    passengers = models.IntegerField()
    travel_class = models.CharField(max_length=10, choices=[('economy', 'Economy'), ('business', 'Business'), ('first', 'First Class')])

    def _str_(self):
        return f"{self.from_location} to {self.to_location} for {self.passengers} passenger(s)"
