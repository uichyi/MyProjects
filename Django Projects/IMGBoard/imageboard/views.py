from crispy_forms.utils import render_crispy_form
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.template.context_processors import csrf

from imageboard.models import *
from imageboard.forms import *
from django.contrib.auth.models import Group, Permission

# Create your views here.

"""
def landing_page(request):
    posts = len(list(Post.objects.filter()))
    users = len(list(User.objects.filter()))
    boards = list(Board.objects.filter())
    return render(request, 'landing.html', {'posts': posts, 'users': users, 'boards': boards})
"""


def show_rules(request):
    return render(request, 'rules.html')


def board_page(request, board_id):
    board_shortcut = Board.objects.get(shortcut=board_id).id
    board_name = Board.objects.get(shortcut=board_id)
    threads = list(Thread.objects.filter(board=board_shortcut))
    boards = list(Board.objects.filter())
    return render(request, f'board/threads.html', {'board_name': board_name, 'threads': threads, 'boards': boards})


def board_add(request, board_id):
    board_shortcut = Board.objects.get(shortcut=board_id).id
    board_name = Board.objects.get(shortcut=board_id)
    threads = list(Thread.objects.filter(board=board_shortcut))
    boards = list(Board.objects.filter())
    if request.method == 'POST':
        form = CreateThread(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(pk=request.user.pk)
            except:
                user = None
            if user is not None:
                if user.is_active:
                    thread_board = Board.objects.get(id=board_name.id)
                    new_thread = form.save(commit=False)
                    new_thread.board = thread_board
                    new_thread.save()
                    form.save_m2m()
                    return render(request, f'board/thread_added.html',
                                  {'board_name': board_name})
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = CreateThread()
        return render(request, f'board/{board_id}/add_thread.html', {'form': form, 'board_name': board_name,
                                                          'threads': threads, 'boards': boards})


def thread_page(request, board_id, thread_id):
    board_name = Board.objects.get(shortcut=board_id)
    thread = Thread.objects.get(id=thread_id)
    post = list(Post.objects.filter(thread_id=thread_id))
    boards = list(Board.objects.filter())
    if request.method == "GET":
        form = CreatePost()
        try:
            user = User.objects.get(pk=request.user.pk)
        except:
            user = None
        if user is not None:
            if user.groups.filter(name="Moderators"):
                return render(request, f'board/{board_id}/moder_thread.html', {'form': form, 'post': post,
                                                                               'thread': thread, 'boards': boards})
        return render(request, f'board/{board_id}/thread.html', {'form': form, 'post': post, 'thread': thread,
                                                                 'boards': boards})
    else:
        form = CreatePost(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(pk=request.user.pk)
            except:
                user = None
            if user is not None:
                if user.is_active:
                    post_thread = Thread.objects.get(id=thread_id)
                    new_post = form.save(commit=False)
                    new_post.username = user
                    new_post.thread = post_thread
                    new_post.save()
                    form.save_m2m()
                    return render(request, f'board/{board_id}/post_added.html',
                                  {'board_name': board_name, 'thread_id': thread_id})
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')


def user_login(request):
    posts = len(list(Post.objects.filter()))
    users = len(list(User.objects.filter()))
    boards = list(Board.objects.filter())
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'landing.html', {'posts': posts, 'users': users, 'boards': boards})
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = UserForm()
        if request.user.is_authenticated:
            return render(request, 'landing.html', {'form': form, 'posts': posts, 'users': users, 'boards': boards})
    return render(request, 'landing_auth.html', {'form': form, 'posts': posts, 'users': users, 'boards': boards})


def user_register(request):
    posts = len(list(Post.objects.filter()))
    users = len(list(User.objects.filter()))
    boards = list(Board.objects.filter())
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            new_user.groups.add(Group.objects.get(name="Users"))
            return render(request, 'register_successful.html', {'new_user': new_user})
    else:
        form = RegistrationForm()
    return render(request, 'landing_register.html', {'form': form, 'posts': posts, 'users': users, 'boards': boards})


def registration_success(request):
    return user_login(request)


def remove_thread(request, board_id, thread_id):
    board_name = Board.objects.get(shortcut=board_id)
    Thread.objects.get(id=thread_id).delete()
    Post.objects.filter(thread=thread_id).delete()
    return render(request, f'board/{board_id}/remove_thread.html', {'board_name': board_name})


def post_created(request, board_id, thread_id):
    return thread_page(request, board_id, thread_id)


def thread_created(request, board_id):
    return board_page(request, board_id)


def validate_username(request):
    username = request.GET.get('username', None)
    response = {
        'taken': User.objects.filter(username__exact=username).exists()
    }
    return JsonResponse(response)
