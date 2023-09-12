from .models import Restaurant, Menu, MenuItem
from .serializers import (
    RestaurantSerializer,
    MenuSerializer,
    MenuItemSerializer,
    MenuCreateSerializer,
    RestaurantRetrieveSerializer,
    MenuRetrieveSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime


class RestaurantList(APIView):
    """
    List all restaurants or create a new restaurant.
    Example POST JSON input data:
    {
        "name": "Chelentano",
        "address": "Sykhivska 21"
    }
    """

    def get(self, request):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RestaurantInfo(APIView):
    """
    Get info for a specific restaurant.
    """

    def get(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        menus = Menu.objects.filter(restaurant=restaurant)
        for menu in menus:
            menu.menu_items = MenuItem.objects.filter(menu=menu)
        menu_serializer = MenuRetrieveSerializer(menus, many=True)
        for field in menu_serializer.data:
            del field["restaurant"]
        serializer = RestaurantRetrieveSerializer(restaurant)
        result = serializer.data
        result["menus"] = menu_serializer.data
        return Response(result)


class MenuList(APIView):
    """
    List all menus for a restaurant or create a new menu.
    """

    def get(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        menus = Menu.objects.filter(restaurant=restaurant)
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuItemList(APIView):
    """
    List all menu items for a menu or add a new one.
    """

    def get(self, request, pk):
        menu = Menu.objects.get(pk=pk)
        menu_items = MenuItem.objects.filter(menu=menu)
        serializer = MenuItemSerializer(menu_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateMenu(APIView):
    """
    Create a new menu for a restaurant.
    Example JSON input data:
    {
        "restaurant": 1,
        "number": 2,
        "day": "2022-04-23",
        "menu_items": [
            {"name": "Burger", "description": "Classic hamburger with beef.", "menu": 2},
            {"name": "Fries", "description": "French fries with garlic sauce.", "menu": 2}
        ]
    }
    """

    def post(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        serializer = MenuCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["restaurant"] = restaurant
            serializer.save()
            return Response({"status": "success"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentDayMenu(APIView):
    """
    View that retrieves a current day menu for a restaurant.
    """

    def get(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        today = datetime.date.today()
        current_menu = Menu.objects.get(restaurant=restaurant, day=today)
        current_menu.menu_items = MenuItem.objects.filter(menu=current_menu)
        serializer = MenuRetrieveSerializer(current_menu)
        return Response(serializer.data, status=status.HTTP_200_OK)
