from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile


#index_view главная страница
def index_view(request):
    
    return render(request,"Blog/index.html")


def login_view(request):
    #Если метод не пост никуда не перенаправляем 
    if request.method != 'POST':
        return render(request, 'Blog/login.html')


    username = request.POST.get('username')
    password = request.POST.get('password')

    # Проверяем введенные логин и пароль на соответствие существующему пользователю
    user = authenticate(request, username=username, password=password)
    if user is not None:
        # Если пользователь найден, выполняем вход
        login(request, user)
        return redirect('/')  # Перенаправляем пользователя на главную при успешной авторизации
    else:
        # Если пользователь не найден, выводим сообщение об ошибке
        error_message = "Неправильный логин или пароль."
        return render(request, 'Blog/login.html', {'error_message': error_message})

    return render(request, 'Blog/login.html')


def logout_view(request):
    logout(request)
    return redirect('/login')  #Url login

def register_view(request):
    if request.method != 'POST':
        return render(request, 'Blog/register.html')


    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email', '')
    first_name = request.POST.get('first_name', '')
    last_name = request.POST.get('last_name', '')
    discription = request.POST.get('discription', '')

    # Создаем нового пользователя
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )

    # Создаем экземпляр UserProfile и привязываем его к созданному пользователю
    user_profile = UserProfile.objects.create(
        user=user,
        discription=discription
    )

    # Авто вход при успешном создании
    user_login = authenticate(username=username, password=password)
    if user_login is not None:
        # Если пользователь успешно аутентифицирован, выполняем вход
        login(request, user_login)

    return redirect('/')  # перенаправляем на главную страницу



def all_blogs(request):



    return render(request, 'Blog/all_blogs.html')


def all_bloggers(request):

    bloggers = UserProfile.objects.all()

    return render(request, 'Blog/all_bloggers.html', {'bloggers' : bloggers})
