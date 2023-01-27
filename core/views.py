import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile


def index(request):
    return render(request, 'index.html')

# doesn't belong to the views.py
# use it it register function


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

    ozon_list = user_model.string_to_json(user_model.ozon_products)
    wb_list = user_model.string_to_json(user_model.wb_products)

    # for home.html; line ~76
    if (len(ozon_list) == 0):
        ozon_list = '[]'

    if (len(wb_list) == 0):
        wb_list = '[]'

    return render(request, 'home.html', {'ozon_list': ozon_list, 'wb_list': wb_list})


def add_product_code(request):

    product_code = request.POST['code']
    if (repeat_checker(request, product_code)):
        return redirect(home)

    response = html_parser(product_code)
    # check if the response is not none

    user = request.user.id
    user_model = Profile.objects.get(id_user=user)
    user_model.fill_storage_wb(response)
    user_model.save()

    return redirect(home)


def repeat_checker(request, id):
    user = request.user.id
    user_model = Profile.objects.get(id_user=user)
    # wb_goods is a string
    wb_goods = user_model.wb_products
    json_wb_goods = user_model.string_to_json(wb_goods)

    for item in json_wb_goods:
        # item[2] is an article
        if (int(item[2]) == id):
            return True

    return False


def html_parser(id):
    url = 'https://www.wildberries.ru/catalog/13158614/detail.aspx'

    def get_new_url(id):
        lst = url.split('/')
        lst[-2] = str(id)
        return '/'.join(lst)

    def create_driver(url):
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(2)
        return driver

    def extract_data(driver):
        good_name = driver.find_element(By.CLASS_NAME, 'product-page__header')
        good_id = driver.find_element(By.ID, 'productNmId')
        return [good_name, good_id]

    def data_uniform(src_lst, full_name):
        # splitting first string into
        # the [brand_name, good_name,] list
        name_list = full_name.split('\n')
        return [name_list[0], name_list[1], src_lst[1].text]

    actual_url = get_new_url(id)
    driver = create_driver(actual_url)
    raw_data_list = extract_data(driver)
    return data_uniform(raw_data_list, raw_data_list[0].text)
