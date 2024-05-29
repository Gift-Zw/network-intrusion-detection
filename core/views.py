from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from core.admin import UserCreationForm
from core.models import User


# Create your views here.

@login_required
def dashboard_view(request):
    context = {
        'user': request.user
    }
    return render(request, 'index.html', context)


@login_required
def logs_view(request):
    context = {}
    return render(request, 'logs.html', context)


@login_required
def users_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                email=form.data['email'],
                first_name=form.data['first_name'],
                last_name=form.data['last_name'],
                password=form.data['password1']
            )
            user.save()
            return redirect('users')
        else:
            messages.error(request, form.errors)
    else:
        form = UserCreationForm()

    context = {
        'users': User.objects.all(),
        'form': UserCreationForm()
    }
    return render(request, 'users.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('dashboard')
