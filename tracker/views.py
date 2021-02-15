from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, CreateTrackItem
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Item


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Username OR password is incorrect")
            return render(request, 'tracker/login.html')
    return render(request, 'tracker/login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account has been created for {username}")
            return redirect('login')
    return render(request, 'tracker/register.html', {'form': form})


@login_required(login_url='login')
def home(request):
    tracked_items = Item.objects.filter(user=request.user)
    tracked_items_number = len(tracked_items)
    items_count = tracked_items.count()
    form = CreateTrackItem(request.POST or None)
    items_discounted = 0
    error = None
    items_discounted_list = []
    if items_count > 0:
        for item in tracked_items:
            if item.current_price < item.old_price:
                items_discounted_list.append(item)
        items_discounted = len(items_discounted_list)
    if request.method == "POST":
        try:
            if form.is_valid():
                url = request.POST.get("url")
                new_item = form.save(commit=False)
                new_item.url = url
                new_item.user = request.user
                new_item.save()
                return redirect('home')
        except AttributeError:
            error = "Couldn't get the name or the price"
        except:
            error = "Something went wrong"
    context = {'tracked_items': tracked_items, 'form': form, 'items_discounted_list:': items_discounted_list,
               'items_discounted': items_discounted, 'error': error, 'tracked_items_number': tracked_items_number}
    return render(request, 'tracker/home.html', context)


@login_required(login_url='login')
def delete_item(request, pk):
    item = get_object_or_404(Item, id=pk)
    if request.method == "POST":
        item.delete()
        return redirect('home')
    return render(request, 'tracker/confirm_del.html', {'item': item})


@login_required(login_url='login')
def update_items(request):
    items = Item.objects.filter(user=request.user)
    for item in items:
        item.save()
    return redirect('home')
