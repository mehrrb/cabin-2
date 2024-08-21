from cabin.models import *
from django.db.models import Count,Sum,F,Q
from django.db.models import F, ExpressionWrapper, DurationField
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D


def query_0(x):
    q = Driver.objects.filter(rating__gt=x)
    return q


def query_1(x):
    
    return Payment.objects.filter(ride__car__owner_id=x).aggregate(total_amount=sum('amount'))['total_amount']


def query_2(x):
    
    # return Ride.objects.filter(request__rider_id=x).select_related('car')
    return Ride.objects.filter(request__rider_id=x)

def query_3(t):
    
    duration = ExpressionWrapper(F('dropoff_time') - F('pickup_time'), output_field=DurationField())
    travels = Ride.objects.filter(duration__gt=t)



def query_4(x, y, r):
    
    point = Point(x, y)
    return Driver.objects.filter(
        active=True,
        location__distance_lte=(point, D(km=r))
    )


def query_5(n, c):
    
    return Driver.objects.filter(Q(car__car_type='A') | Q(car__color=c), rides__count__gte=n).distinct()


def query_6(x, t):
    return Rider.objects.filter(riders__count_gte=x)


def query_7():
    q = 'your query here'
    return q


def query_8():
    q = 'your query here'
    return q


def query_9(n, t):
    q = 'your query here'
    return q


def query_10():
    q = 'your query here'
    return q
