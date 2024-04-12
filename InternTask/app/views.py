from django.shortcuts import render
from django.http import JsonResponse

from app.forms import *
from app.models import *

# Create your views here.


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                user = DBUser.objects.get(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                if user is not None:
                    clients = Client.objects.filter(responsible=user)
                    return render(request, 'show_table.html', {'clients': clients, 'user': user})
            except:
                form = LoginForm()
                return render(request, 'landing.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'landing.html', {'form': form})


def update_status(request):
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        status = request.POST.get('status')
        client = Client.objects.get(accountNumber=account_number)
        client.status = status
        client.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})
