from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile, UserPost, Comment
from django.core.paginator import Paginator


#index_view главная страница
def index_view(request):
    posts = UserPost.objects.all() # Получаем все записи из таблицы UserPost
    
    paginator = Paginator(posts, 20)  # Разбиваем на страницы по 5 элементов
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Blog/index.html', {'page_obj': page_obj})


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

    # Если пользователь не найден, выводим сообщение об ошибке
    error_message = "Неправильный логин или пароль."
    return render(request, 'Blog/login.html', {'error_message': error_message})


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
    description = request.POST.get('description', '')

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
        description=description
    )

    # Авто вход при успешном создании
    user_login = authenticate(username=username, password=password)
    if user_login is not None:
        # Если пользователь успешно аутентифицирован, выполняем вход
        login(request, user_login)

    return redirect('/')  # перенаправляем на главную страницу


# Отображение страницы для всех блогов
def all_blogs(request):

    posts = UserPost.objects.all() # Получаем все записи из таблицы UserPost
    
    paginator = Paginator(posts, 5)  # Разбиваем на страницы по 5 элементов
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Blog/all_blogs.html', {'page_obj': page_obj})


# Профиль
def profile_view(request, user_id):

    user_profile = UserProfile.objects.get(user_id=user_id) # Получаем Запись пользователя по его id
    user_posts = UserPost.objects.filter(user=user_profile.user).order_by('date') # Получаем все посты этого пользователя 

    paginator = Paginator(user_posts, 5)  # Разбиваем на страницы по 5 элементов
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    return render(request, 'Blog/profile.html', {'user_profile': user_profile, 'user_posts': page_posts})

# Страница одного поста
def post_view(request, post_id):

    post = get_object_or_404(UserPost, id=post_id)

    comments = Comment.objects.filter(post=post).order_by('date') # Получаем все комментарии и сортируем по дате
    
    paginator = Paginator(comments, 5)  # Разбиваем на страницы по 5 элементов
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Blog/post.html', {'post': post, 'comments': page_obj})


# Страница комментария
def comment_view(request, post_id):

    post = get_object_or_404(UserPost, id=post_id)

    if request.method != "POST":
        
        return render(request, 'Blog/comment.html', {'post': post})

    # Написать обработчик добавления комментария 

    user = request.user.username
    description = request.POST.get('description', '')
    comment = Comment(
            name=description[:20],
            post=post,
            user=request.user,
            description=description,)
    comment.save()

    return redirect('post', post_id=post.id)


# Все пользователи
def all_bloggers(request):

    bloggers = UserProfile.objects.all() # Получаем всех пользователей
    
    paginator = Paginator(bloggers, 5)  # Разбиваем на страницы по 5 элементов
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'Blog/all_bloggers.html', {'page_obj': page_obj})
