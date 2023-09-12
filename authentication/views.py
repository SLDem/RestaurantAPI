from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .forms import SignupForm
from .models import User
from .serializers import UserSerializer


def signup(request):
    title = "Signup"

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            raw_password = form.cleaned_data.get("password1")
            name = form.cleaned_data["name"]
            user.is_active = True
            user = User.objects.create(
                email=user.email, password=raw_password, name=name
            )
            user.set_password(raw_password)
            user.save()

            return redirect("login")
    else:
        form = SignupForm()
    return render(request, "authentication/signup.html", {"form": form, "title": title})


class EmployeeList(APIView):
    """
    List all employees or create a new employees.
    Example POST JSON input data:
    {
        "email": "example2@gmail.com",
        "name": "James Rambo",
        "restaurant": 1,
        "password": "password"
    }
    """

    def get(self, request):
        employees = User.objects.all()
        serializer = UserSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
