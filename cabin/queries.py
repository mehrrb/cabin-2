from django.db.models import Sum, Count, F, ExpressionWrapper, FloatField, Q
from .models import Account, Admin, Rider, Driver, Car, RideRequest, Ride, Payment
from datetime import timedelta

def query_1(x):
    
    return Payment.objects.filter(ride__car__owner_id=x).aggregate(payment_sum=Sum('amount'))

def query_2(x):
    
    return Ride.objects.filter(request__rider_id=x)

# def query_3(t):
    
#     return Ride.objects.annotate(duration=F("dropoff_time") - F("pickup_time")).filter(duration__gt=t).count()

def query_3(t):
    duration_threshold = timedelta(milliseconds=t)  # تغییر مقدار به timedelta
    return Ride.objects.annotate(duration=F("dropoff_time") - F("pickup_time")).filter(duration__gt=duration_threshold).count()


def query_4(x, y, r):
    
    return Driver.objects.annotate(
        loc=ExpressionWrapper(
            ((F("x") - x) ** 2) + ((F("y") - y) ** 2), output_field=FloatField()
        )
    ).filter(active=True, loc__lt=r**2)

def query_5(n, c):
    
    return Driver.objects.annotate(ride_num=Count("car__ride")).filter(Q(car__color=c) | Q(car__car_type="A")).filter(ride_num__gte=n)

def query_6(x, t):
    return Rider.objects.annotate(
        ride_num=Count("riderequest__ride"),
        total_pay=Sum("riderequest__ride__payment__amount"),
    ).filter(ride_num__gte=x, total_pay__gt=t)
    

def query_7():

    return Driver.objects.filter(account__first_name=F("car__ride__request__rider__account__first_name"))

def query_8():
    
    return Driver.objects.annotate(
        n=Count('car__ride', filter=Q(account__last_name=F("car__ride__request__rider__account__last_name")),)
    )

def query_9(x, t):
    # TODO: not working
    s = Ride.objects.annotate(duration=F("dropoff_time") - F("pickup_time")).filter(
        duration__gt=t, car__model__gte=x
    )
    q = Driver.objects.annotate(n=Count("car__ride", filter=Q(car__ride__in=s))).values(
        "id", "n"
    )
    return q

def query_10():
    q = Car.objects.annotate(
        extra=Case(
            When(
                car_type="A",
                then=Count("ride"),
            ),
            When(
                car_type="B", then=Sum(F("ride__dropoff_time") - F("ride__pickup_time"))
            ),
            When(car_type="C", then=Sum("ride__payment__amount")),
            output_field=IntegerField(),
        )
    )
    return q
