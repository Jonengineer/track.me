from django.shortcuts import render

def base_page(request):
    # Базовая страница
    return render(request, 'base_page.html')
