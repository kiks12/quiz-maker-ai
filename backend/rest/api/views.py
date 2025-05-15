from django.shortcuts import render
from rest_framework.decorators import api_view


@api_view(["POST"])
def send_message(request):
    if request.method == "POST":
        print("POST")
