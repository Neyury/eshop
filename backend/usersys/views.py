from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf
from catalog.models import ProductCategory


def login(request):
    category_list = ProductCategory.objects.all()

    context = {
        'category_list': category_list,
        'form':  UserCreationForm(),
    }
    context.update(csrf(request))
    if request.method == 'POST':
        username = request.POST.get('login', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            context['login_error'] = 'Пользователь не найден'
            return render(request, 'usersys/login.html', context)
    else:
        return render(request, 'usersys/login.html', context)


def logout(request):
    auth.logout(request)
    return redirect('/')


def registration(request):
    category_list = ProductCategory.objects.all()
    context = {
        'category_list': category_list,
        'form':  UserCreationForm(),
    }
    context.update(csrf(request))
    if request.method == 'POST':
        nu_form = UserCreationForm(request.POST)
        if nu_form.is_valid():
            nu_form.save()
            newuser = auth.authenticate(
                username=nu_form.cleaned_data['username'],
                password=nu_form.cleaned_data['password2']
            )
            auth.login(request, newuser)
            return redirect('/')
        else:
            context['login_error'] = 'Пользователь не найден'
            return render(request, 'usersys/registration.html', context)
    else:
        return render(request, 'usersys/registration.html', context)