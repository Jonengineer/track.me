from django.shortcuts import render, redirect
from .models import User, UserType
from .forms import UserForm, UserProfileForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import password_validation
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Представление для создания формы регистрации пользователей
def create_user(request):
    usertypes = UserType.objects.all()
    age_people = ["Не указан"]
    age_people.extend([str(year) for year in range(0, 121)])

    if request.method == 'POST':
        if request.POST.get('userage') == "Не указан":
            request.POST=request.POST.copy()
            request.POST['userage'] = None

        if User.objects.filter(email=request.POST['email']).exists():
            return JsonResponse({
                "success": False,
                "errors": {'email': 'Пользователь с таким Email уже зарегистрирован.'}
            }, content_type="application/json; charset=utf-8") # Возвращаем успешный ответ в формате JSON
                    
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
        # Проверка валидации пароля
            errors = {}
            try:
                password_validation.validate_password(user_form.cleaned_data['password'], user)
            except password_validation.ValidationError as e:
                errors['password'] = list(e.messages)

            if errors:
                return JsonResponse({"success": False, "errors": errors})
        
            
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            # Если пароль валиден, сохраняем пользователя и профиль
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()  

            return JsonResponse({"success": True})
        else:
            # Соберите ошибки из форм и верните их в ответе
            errors = {}
            for field, error in user_form.errors.items():
                errors[field] = error[0]
            for field, error in profile_form.errors.items():
                errors[field] = error[0]

            return JsonResponse({"success": False, "errors": errors})
            
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context = {
        'user_form': user_form, 
        'profile_form': profile_form, 
        'usertypes': usertypes,
        'age_people': age_people  # Добавьте эту строку
    }
    return render(request, 'create_user.html', context)  


def user_login(request):
    if request.user.is_authenticated:
            return redirect('User:user_profile')
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('User:user_profile')
        else:
            error_message = 'Неверный пароль или email.Проверьте данные и попробуйте еще раз.'
            messages.error(request, error_message)

            # Возвращаем JSON-ответ с сообщением об ошибке
            response_data = {
                'success': False,
                'error_message': error_message
            }
            return JsonResponse(response_data)
    return render(request, 'user_login.html', {'user': request.user})
    
@login_required
def user_log_out(request):
    logout(request)
    return redirect('AppBase:base_page')


# Профиль пользователя
@login_required
def user_profile(request):
    # Базовая страница
    return render(request, 'user_profile.html')


