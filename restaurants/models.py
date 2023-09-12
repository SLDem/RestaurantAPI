from django.db import models
import datetime


class Restaurant(models.Model):
    """
    Model for creating restaurants.
    """

    objects = models.Manager()

    name = models.CharField(max_length=50)
    address = models.CharField(max_length=400)

    def __str__(self):
        return self.name


class Menu(models.Model):
    """
    Model for creating menus.
    """

    objects = models.Manager()

    number = models.IntegerField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    day = models.DateField(default=datetime.date.today(), unique=True)

    def __str__(self):
        return "Menu #{} for restaurant {}".format(self.number, self.restaurant.name)


class MenuItem(models.Model):
    """
    Model for creating menu items.
    """

    objects = models.Manager()

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
