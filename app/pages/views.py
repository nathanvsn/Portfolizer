from django.shortcuts import render

def home(request):
    return render(request, 'pages/pages/home.html')

def about(request):
    return render(request, 'pages/pages/about.html')

def privacy(request):
    return render(request, 'pages/pages/privacy.html')

def terms(request):
    return render(request, 'pages/pages/terms.html')
