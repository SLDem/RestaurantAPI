from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from restaurants.models import Restaurant, Menu, MenuItem
from restaurants.serializers import RestaurantSerializer, MenuSerializer
import datetime


class RestaurantCreateTest(APITestCase):
    def test_create_restaurant(self):
        url = reverse("restaurants")
        data = {"name": "test name", "address": "test address"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(Restaurant.objects.get().name, "test name")


class MenuCreateTest(APITestCase):
    def test_create_menu(self):
        restaurant = Restaurant.objects.create(name="test name", address="test address")
        serializer = RestaurantSerializer(data=restaurant)

        url = reverse("menus", kwargs={"pk": restaurant.pk})

        if serializer.is_valid():
            data = {
                "number": 1,
                "day": "2023-09-12",
                "restaurant": serializer.validated_data,
            }
            response = self.client.post(url, data, format="json")

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Menu.objects.count(), 1)
            self.assertEqual(Menu.objects.get().name, "test")


class MenuItemCreateTest(APITestCase):
    def test_create_menu_item(self):
        restaurant = Restaurant.objects.create(name="test", address="test")
        menu = Menu.objects.create(number=1, restaurant=restaurant, day="2023-09-12")

        serializer = MenuSerializer(data=menu)

        url = reverse("menu_items", kwargs={"pk": menu.pk})

        if serializer.is_valid():
            data = {
                "name": "test item",
                "description": "test description",
                "menu": menu,
            }
            response = self.client.post(url, data, format="json")

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Restaurant.objects.count(), 1)
            self.assertEqual(Restaurant.objects.get().name, "test_restaurant_name")


class CurrentMeuRetrieveTest(APITestCase):
    def test_retrieve_current_menu(self):
        restaurant = Restaurant.objects.create(name="test", address="test")
        menu = Menu.objects.create(
            number=1, restaurant=restaurant, day=datetime.date.today()
        )
        MenuItem.objects.create(
            name="test item", description="test description", menu=menu
        )

        url = reverse("current_day_menu", kwargs={"pk": restaurant.pk})
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        self.assertContains(response, "test item")
