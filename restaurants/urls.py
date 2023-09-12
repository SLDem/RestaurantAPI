from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path("restaurants/", views.RestaurantList.as_view(), name="restaurants"),
    path("restaurant/<int:pk>/", views.RestaurantInfo.as_view(), name="restaurant"),
    path("menus/<int:pk>/", views.MenuList.as_view(), name="menus"),
    path("menu_items/<int:pk>/", views.MenuItemList.as_view(), name="menu_items"),
    path("create_menu/<int:pk>/", views.CreateMenu.as_view(), name="create_menu"),
    path(
        "current_day_menu/<int:pk>/",
        views.CurrentDayMenu.as_view(),
        name="current_day_menu",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
