from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from users.models import Account

# Choices for car types
car_type_choices = (
    ('A', 'Class A'),
    ('B', 'Class B'),
    ('C', 'Class C'),
)

class Admin(models.Model):
    account = GenericRelation(Account, related_query_name='admins')

class Rider(models.Model):
    account = GenericRelation(Account, related_query_name='riders')
    rating = models.FloatField()
    x = models.FloatField()
    y = models.FloatField()

class Driver(models.Model):
    account = GenericRelation(Account, related_query_name='drivers')
    rating = models.FloatField()
    x = models.FloatField()
    y = models.FloatField()
    active = models.BooleanField(default=False)

class RideRequest(models.Model):
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    x = models.FloatField()
    y = models.FloatField()
    car_type = models.CharField(max_length=3, choices=car_type_choices)

class Car(models.Model):
    owner = models.ForeignKey(Driver, on_delete=models.CASCADE)
    car_type = models.CharField(max_length=3, choices=car_type_choices)
    model = models.IntegerField()
    color = models.CharField(max_length=10)

class Ride(models.Model):
    pickup_time = models.DateTimeField()
    dropoff_time = models.DateTimeField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    request = models.OneToOneField(RideRequest, on_delete=models.CASCADE)
    rider_rating = models.FloatField()
    driver_rating = models.FloatField()

class Payment(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    amount = models.FloatField()
    status = models.IntegerField()  # For example: 0 - Completed, 1 - Pending
