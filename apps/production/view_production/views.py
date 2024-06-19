from django.shortcuts import render
from ...users.forms import LoginForm
from django.contrib.auth import login, authenticate
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from apps.production import forms, views


# @method_decorator(login_required)
def main_view(request):
    # print(request)
    if not request.user.is_authenticated:
        print(request)
        form = LoginForm()
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                )
                # message = ''
                if user is not None:
                    login(request, user)
                    # t = loader.get_template("main.html")
                    return HttpResponseRedirect('')
                    # return render(request, 'main.html')
                    # message = f'Hello {user.username}! You have been logged in'
                else:
                    message = 'Login failed!'
                    return render(request, 'login.html', context={'form': form})
        elif request.method == 'GET':
            return render(request, 'login.html', context={'form': form})
                # print(form)
    else:
        print('ina')
        form = forms.BoxModelForm
        return render(request, 'main.html', context={'form': form})