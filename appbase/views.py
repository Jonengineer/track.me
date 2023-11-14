from django.shortcuts import render

def base_page(request):
    # Базовая страница
    return render(request, 'base_page.html')


def main_skrin_page(request):
    # Базовая страница
    return render(request, 'main_skrin.html')
