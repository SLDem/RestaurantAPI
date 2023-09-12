from rest_framework import serializers
from .models import Restaurant, Menu, MenuItem


class RestaurantSerializer(serializers.ModelSerializer):
    """
    Serializer to create restaurants and retrieve their base data.
    """

    name = serializers.CharField(max_length=50)
    address = serializers.CharField(max_length=400)

    class Meta:
        model = Restaurant
        fields = "__all__"


class MenuItemSerializer(serializers.ModelSerializer):
    """
    Serializer to create menu items and retrieve their base data.
    """

    name = serializers.CharField()
    description = serializers.CharField()
    menu = serializers.CharField()

    class Meta:
        model = MenuItem
        fields = ["name", "description", "menu"]


class MenuSerializer(serializers.ModelSerializer):
    """
    Serializer to create menus and retrieve their base data.
    """

    restaurant = serializers.CharField(source="restaurant.name")

    class Meta:
        model = Menu
        fields = "__all__"


class RestaurantRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer to retrieve in-depth data about a single restaurant.
    """

    menus = MenuSerializer(read_only=True, many=True)

    class Meta:
        model = Restaurant
        fields = ["name", "address", "menus"]


class MenuRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer to retrieve data about menu and its items.
    """

    menu_items = MenuItemSerializer(read_only=True, many=True)

    class Meta:
        model = Menu
        fields = "__all__"


class MenuCreateSerializer(serializers.ModelSerializer):
    """
    Serializer to create menus alongside menu items.
    """

    number = serializers.IntegerField()
    day = serializers.DateField()
    menu_items = MenuItemSerializer(many=True)

    def create(self, validated_data):
        menu_items_data = validated_data.pop("menu_items")
        menu = Menu.objects.create(**validated_data)
        for menu_item_data in menu_items_data:
            del menu_item_data["menu"]
            MenuItem.objects.create(menu=menu, **menu_item_data)
        return menu

    class Meta:
        model = Menu
        fields = ["number", "day", "menu_items"]
