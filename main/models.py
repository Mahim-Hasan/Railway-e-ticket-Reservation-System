from django.contrib.auth.models import User
from django.db import models


class Train(models.Model): 
    name = models.CharField(max_length=50)
    seats = models.IntegerField()

    def __str__(self):
        return self.name

class Start(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class End(models.Model):
    name = models.CharField(max_length=50)
    distance = models.FloatField()
    start = models.ForeignKey(Start, on_delete=models.CASCADE)
    train = models.ManyToManyField(Train)

    def __str__(self):
        return self.name
    
class Ticket(models.Model):
    ticket_no = models.CharField(max_length=20)
    start = models.CharField(max_length=20)
    end = models.CharField(max_length=20)
    total_seats = models.IntegerField()
    class_type = models.CharField(max_length=20)
    cost = models.IntegerField()
    travel_time = models.DateTimeField() 
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    passenger = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.ticket_no
