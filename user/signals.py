from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    # Получите IP-адрес пользователя из запроса
    user_ip = request.META.get('REMOTE_ADDR')

    # Получите текущую историю входов пользователя
    login_history = user.login_history 
    
    # Добавьте новую запись в историю входов
    login_history.append({
        'timestamp': timezone.now().isoformat(),
        'ip_address': user_ip,
    })

    # Обновите поля в модели пользователя
    user.login_history = login_history
    user.last_login_time = timezone.now()
    user.last_login_ip = user_ip
    user.save()