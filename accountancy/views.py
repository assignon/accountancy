from django.shortcuts import render


def login(request):
    return render(request, template_name='index.html')


def dashboard(request):
    return render(request, template_name='index.html')


def orders(request):
    return render(request, template_name='index.html')


def expenses(request):
    return render(request, template_name='index.html')
