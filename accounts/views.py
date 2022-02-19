from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.db.models import Sum
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import Loading, Company, Producer, Truck
from .forms import LoadingForm, CreateUserForm, CompanyForm
from ._filters import LoadingFilter
from .decorators import unauthenticated_user, allowed_users, admin_only


@login_required(login_url='login')
@allowed_users(allowed_roles=['staff', 'admin'])
def accountSettings(request):
    company = request.user.company
    form = CompanyForm(instance=company)

    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['staff', 'admin'])
def userPage(request: HttpRequest) -> HttpResponse:
    loadings = Loading.objects.filter(truck__producer__company__user=request.user.id)
    context = dict(loadings=loadings)
    return render(request, 'accounts/user.html', context)


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='staff')
            user.groups.add(group)
            Company.objects.create(
                user=user,
                name=username,

            )

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request: HttpRequest) -> HttpResponse:
    context = dict(companies=Company.objects.all(),
                   loadings=Loading.objects.all(),
                   producers=Producer.objects.all(),
                   total_companies=Company.objects.all().count(),
                   total_loadings=Loading.objects.all().count(),
                   pending=Loading.objects.all().filter(status='Pending').count(),
                   finished=Loading.objects.all().filter(status='Finished').count(),
                   )
    return render(request, 'accounts/dashboard.html', context=context)


@login_required(login_url='login')
def loadings(request: HttpRequest) -> HttpResponse:
    context = dict(loadings=Loading.objects.all())
    return render(request, 'accounts/loadings.html', context=context)


@login_required(login_url='login')
def company(request: HttpRequest, pk_test) -> HttpResponse:
    company = Company.objects.get(id=pk_test)
    loadings = Loading.objects.all().filter(truck__producer__company=company.id)
    loadings_sum = loadings.aggregate(Sum('quantity'))
    myFilter = LoadingFilter(request.GET, queryset=loadings)
    loadings = myFilter.qs

    context = dict(
        loadings=loadings,
        company=company,
        loadings_sum=loadings_sum.get('quantity__sum'),
        filter=myFilter,
    )
    return render(request, 'accounts/company.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_loading(request: HttpRequest, pk: int) -> HttpResponse:
    company = Company.objects.get(id=pk)
    form = LoadingForm(company=company)
    if request.method == 'POST':
        form = LoadingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = dict(form=form)
    return render(request, 'accounts/loading_form.html', context=context)


@login_required(login_url='login')
def update_loading(request: HttpRequest, pk: str) -> HttpResponse:
    load = Loading.objects.get(id=int(pk))
    form = LoadingForm(instance=load)
    if request.method == 'POST':
        form = LoadingForm(request.POST, instance=load)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = dict(form=form)
    return render(request, 'accounts/loading_form.html', context=context)


@login_required(login_url='login')
def delete_loading(request: HttpRequest, pk: str) -> HttpResponse:
    load: Loading = Loading.objects.get(id=int(pk))
    if request.method == 'POST':
        load.delete()
        return redirect('/')
    context = dict(item=load)
    return render(request, 'accounts/delete.html', context=context)
