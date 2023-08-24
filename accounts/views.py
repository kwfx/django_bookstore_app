from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy


# class SignupPageView(CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'account/signup.html'


# class LogOutPageView(TemplateView):
#     template_name = 'account/logout.html'
