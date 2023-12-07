from typing import AsyncContextManager
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from rest_framework_api_key.models import APIKey
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, TransactionSerializer
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
from .models import *
from .forms import CreateUserForm, ProfileModelForm

CustomUser = get_user_model()


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


class CustomUserAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'bills/cashout.html'

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     return Response({'user': self.object})

    def post(self, request, *args, **kwargs):
        request.session['username'] = request.POST.get('username')
        request.session['user_id'] = request.POST.get('user_id')
        request.session['redirect_url'] = request.POST.get('redirect_url')
        request.session['email'] = request.POST.get('email')
        request.session['transaction_Pin'] = request.POST.get(
            'transaction_Pin')
        request.session['balance'] = request.POST.get('balance')
        request.session['user_url'] = request.POST.get('user_url')
        request.session['profile_url'] = request.POST.get('profile_url')
        username = request.POST.get('username')
        user = CustomUser.objects.filter(username=username).first()
        print(user)
        if user is None:
            return super().post(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('pay'))
        # print(request.session.get('email'))
        # if user is None:
        #     return HttpResponseRedirect(reverse('create_pin'))


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def home(request):
    if request.user.is_anonymous:
        return redirect("login")

    profile = request.user
    user = CustomUser.objects.get(username=profile.username)
    context = {'profile': profile, 'user': user}
    return render(request, 'accounts/organisation.html', context)


def editProfile(request):
    if request.method == "POST":
        profile_form = ProfileModelForm(request.POST)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile was succesfully updated')
            return redirect("home")
    else:
        profile_form = ProfileModelForm()

    context = {'profile_form': profile_form}
    return render(request, 'accounts/profile.html', context)


def apiRequest(request):
    return render(request, 'accounts/api_request.html')
