from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile


def index(request):
    return render(request, 'index.html')

# doesn't belong to the views.py
# use it it register function


def password_security(pw):
    pass


def register(request):

    if request.method == 'POST':
        username = request.POST['register_username']
        email = request.POST['register_email']
        pw1 = request.POST['register_pw']
        pw2 = request.POST['register_repeat_pw']

        if pw1 != pw2:
            messages.info(request, 'Пароли не совпадают')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.info(request, 'Такая почта уже используется')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Такой логин уже использутеся')
            return redirect('register')

        user = User.objects.create_user(
            username=username, email=email, password=pw1)
        user.save()

        # log user in
        user = auth.authenticate(username=username, password=pw1)
        auth.login(request, user)

        # create a Profile object for a new user
        user_model = User.objects.get(username=username)
        new_profile = Profile.objects.create(
            user=user_model, email=user_model.email, id_user=user_model.id)
        new_profile.save()

        return redirect('/home')

    return render(request, 'register.html')


def login(request):

    if (request.method == 'POST'):

        login = request.POST['login_id']
        pw = request.POST['login_pw']

        user = None
        user = auth.authenticate(username=login, password=pw)

        if (user is None):
            messages.info(request, 'Данные введены неправильно')
            return render(request, 'login.html')

        auth.login(request, user)
        return redirect('/home')

    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required(login_url='login')
def home(request):
    user = request.user.id
    user_model = Profile.objects.get(id_user=user)
    ozon_lst = []
    wb_lst = []

    ozon_bool = False
    wb_bool = False
    if len(user_model.ozon_products) == 0:
        ozon_lst.append('Вы пока не добавляли товаров')
        ozon_bool = True
    if len(user_model.wb_products) == 0:
        wb_lst.append('Вы пока не добавляли товаров')
        wb_bool = True

    if ozon_bool == False:
        ozon_lst = user_model.ozon_products.split('\n')
    if wb_bool == False:
        wb_lst = user_model.wm_products.split('\n')

    return render(request, 'home.html', {'ozon_list': ozon_lst, 'wb_list': wb_lst})
