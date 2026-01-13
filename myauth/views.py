# Create your views here.
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy


# class MyLogoutView(LogoutView):
#     next_page = reverse_lazy("myauth:login")
#
#     def get(self, request, *args, **kwargs):
#         return self.post(request, *args, **kwargs)

def logout_view(request):
    """
    Logs out the current user and redirects to the main page.
    Also displays a success message.
    """
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect(reverse_lazy("myauth:login"))
