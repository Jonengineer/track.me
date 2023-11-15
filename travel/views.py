from django.shortcuts import render, redirect, get_object_or_404
from .form import TravelPlanformTrue
from .models import travelplan, traveltype, Friendship, travelplan_geo
import os
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .gpx_processing import parse_gpx_data
from django.db.models import Q
from datetime import datetime
import json
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_POST
import logging
from PIL import Image

logger = logging.getLogger(__name__)


@login_required
def create_travel_plan(request):
    form = TravelPlanformTrue()
    # Если форма отправлена методом POST, то мы создаем экземпляр формы  с данными
    if request.method == 'POST':

        form = TravelPlanformTrue(request.POST, request.FILES)

        # Если форма валидна, сохраняем данные в базу данных
        if form.is_valid():
            # Создаем экземпляр модели travelplan с данными из формы
            travel_plan = form.save(commit=False)

            # Получаем файл GPX из формы
            gpx_file = request.FILES.get('gpxtrek')

            # Получаем файл JPX из формы
            image_file = request.FILES.get('image')
            if image_file:
                if not image_file.name.endswith('.jpg'):
                    messages.error(
                        request, "Неверный формат файла. Пожалуйста, загрузите jpg файл.")
                    return render(request, 'create_travel_plan.html', {'form': form, 'traveltypes': traveltype.objects.all()})
                try:
                    # Сохраняем изображение в папку
                    image_path = import_imge(image_file)
                    travel_plan.image = image_path
                    # Дальнейшая обработка
                except Exception as e:
                    # Обработка исключения
                    messages.error(
                        request, "Произошла ошибка при обработке jpg файла: {}".format(e))
                    return render(request, 'create_travel_plan.html', {'form': form, 'traveltypes': traveltype.objects.all()})

             # Обрабатываем файл GPX, считываем его содержимое
            gpx_file = request.FILES.get('gpxtrek')
            if gpx_file:
                if not gpx_file.name.endswith('.gpx'):
                    messages.error(
                        request, "Неверный формат файла. Пожалуйста, загрузите GPX файл.")
                    return render(request, 'create_travel_plan.html', {'form': form, 'traveltypes': traveltype.objects.all()})
                try:
                    # Обработка gpx_file
                    gpxtrek = gpx_file.read().decode('utf-8')
                    gpx_statistics = parse_gpx_data(gpxtrek)
                    # Дальнейшая обработка
                except Exception as e:
                    # Обработка исключения
                    messages.error(
                        request, "Произошла ошибка при обработке GPX файла: {}".format(e))
                    return render(request, 'create_travel_plan.html', {'form': form, 'traveltypes': traveltype.objects.all()})

            # Вызываем gpx_data_travel_static для анализа данных GPX
            gpx_statistics = parse_gpx_data(gpxtrek)

            # Конвертируем time_points в строки, если они являются объектами datetime
            time_points_str = [tp.strftime('%Y-%m-%dT%H:%M:%S')
                               for tp in gpx_statistics['time_points']]

            # Записываем статистические данные в соответствующие поля модели
            travel_plan.total_distance_travelled = gpx_statistics['total_distance_travelled']
            travel_plan.total_time_seconds = gpx_statistics['total_time_seconds']
            travel_plan.moving_time_seconds = gpx_statistics['moving_time_seconds']
            travel_plan.speed_midle = gpx_statistics['speed_middle']
            travel_plan.speed_moving = gpx_statistics['speed_moving']
            travel_plan.total_ascent = gpx_statistics['total_ascent']
            travel_plan.total_descent = gpx_statistics['total_descent']

            # Сохраняем содержимое файла GPX в модели  travel_plan_geo

            travel_plan_geo = travelplan_geo()
            travel_plan_geo.gpxtrek = gpxtrek
            travel_plan_geo.graph_data = {
                'time_points': time_points_str,
                'elevation_points': gpx_statistics['elevation_points'],
                'heart_rate_points': gpx_statistics['heart_rate_points'],
                'distances': gpx_statistics['distances'],
            }
            travel_plan_geo.geojson = gpx_statistics['geojson']
            travel_plan_geo.save()

            # Связываем travel_plan с travel_plan_geo
            travel_plan.travelplan_geo = travel_plan_geo

           # Получаем дату и время из формы и парсим их в объект datetime
            travel_plan.datestart = form.cleaned_data['datestart']
            travel_plan.datefinish = form.cleaned_data['datefinish']

            # Вычисляе общее количество дней путешевствия
            difference_data = travel_plan.datefinish - travel_plan.datestart
            travel_plan.quantitydays = difference_data.days

            # Связываем текущего пользователя с планом путешествия
            travel_plan.user = request.user

            # Сохраняем экземпляр модели в базе данных
            travel_plan.save()
            messages.success(request, "Путешевствие создано успешно!")
            return redirect('travel:get_travel_plan')

    else:
        # Если форма не отправлена методом POST, создаем пустую форму
        print(form.errors)
        form = TravelPlanformTrue()
    # Отображаем шаблон с формой, передавая форму в контексте
    return render(request, 'create_travel_plan.html', {'form': form, 'traveltypes': traveltype.objects.all()})


@login_required
def map_page(request):
    # Страница с картой
    current_user = request.user

    return render(request, 'map_page.html')


@login_required
def get_travel_plan(request):
    # Страница с карточками путешевствий
    current_user = request.user

    # Получение данных только для текущего пользователя
    travel = travelplan.objects.filter(user=current_user)

    return render(request, 'get_travel_plan.html', {'travel': travel})


def import_imge(file, output_size=(400, 267)):
    if file is None:
        return None
    try:
        # Путь и имя файла для сохранения
        base_name = os.path.splitext(file.name)[0]  # без расширения
        file_name = os.path.join('travelfoto', file.name)
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        # Создаем директорию, если она не существует
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Открываем файл изображения с помощью Pillow
        image = Image.open(file)

        # Меняем размер изображения
        image = image.resize(output_size, Image.Resampling.LANCZOS)

        # Сжимаем изображение и сохраняем
        # Определяем качество сжатия
        quality_val = 85
        image.save(file_path, image.format, quality=quality_val, optimize=True)

        media_url = os.path.join(
            settings.MEDIA_URL, 'travelfoto', file.name).replace('\\', '/')

        return media_url
    except IOError:
        print("Ошибка при обработке изображения")
        return None

    except TypeError as e:
        print(f"Error: {e}")
        print(f"settings.MEDIA_ROOT: {settings.MEDIA_ROOT}")
        print(f"fileName: {file_name}")
        return None


@login_required
def travel_detail_chart(request, travelplan_id):
    # Страница путешевствий
    # Получаем путешествие из базы данных
    travelplan_instance = get_object_or_404(travelplan, pk=travelplan_id)

    # Проверяем, принадлежит ли путешествие текущему пользователю
    if travelplan_instance.user == request.user:
        pass
    elif travelplan_instance.is_public:
        pass
    elif travelplan_instance.friends_only:
        # Проверка на дружбу между текущим пользователем и владельцем путешествия
        friendship_exists = Friendship.objects.filter(
            (Q(user1=request.user) & Q(user2=travelplan_instance.user)) |
            (Q(user1=travelplan_instance.user) & Q(user2=request.user))
        ).exists()
        if not friendship_exists:
            return HttpResponse('У Вас нетдоступа к данному плану путешествия')
    else:
        return HttpResponse('У Вас нетдоступа к данному плану путешествия')
    
    # Проверяем, есть ли связанный travelplan_geo
    if hasattr(travelplan_instance, 'travelplan_geo'):
       travelplan_geo_instance = travelplan_instance.travelplan_geo

    # Обрабатываем данные GPX, если они имеются
    if travelplan_geo_instance.graph_data:
        processed_gpx_data = travelplan_geo_instance.graph_data
        # преобразовываем время, если оно имеется в processed_gpx_data
        # if 'time_points' in processed_gpx_data:
        # processed_gpx_data['time_points'] = [convert_to_iso_format(time_str) for time_str in processed_gpx_data['time_points']]
    else:
        processed_gpx_data = {}

        # Обрабатываем данные GPX, если они имеются
    if travelplan_geo_instance.geojson:
        track_coordinates = travelplan_geo_instance.geojson
        # преобразовываем время, если оно имеется в processed_gpx_data
        # if 'time_points' in processed_gpx_data:
        # processed_gpx_data['time_points'] = [convert_to_iso_format(time_str) for time_str in processed_gpx_data['time_points']]
    else:
        track_coordinates = {}

    context = {
        'travel': travelplan_instance,
        'gpx_data': json.dumps(processed_gpx_data),
        'gpx_data_track': json.dumps(track_coordinates),
    }
    return render(request, 'travel_detail_chart.html', context)


def convert_to_iso_format(time_element):
    # Преобразование времени для графиков
    # Если это уже объект datetime, просто преобразуйте в формат ISO
    if isinstance(time_element, datetime):
        return time_element.isoformat() + "Z"
    # В противном случае анализируйте его из данного строкового формата
    return datetime.strptime(time_element, '%b. %d, %Y, %I:%M %p').isoformat() + "Z"


@login_required
def delete_travel_plan(request, travelplan_id):
    # Удаление планов путешевствий
    logger.info("Запрос на удаление плана путешествия с ID: %s", travelplan_id)

    travel_plan = get_object_or_404(travelplan, pk=travelplan_id, user=request.user)

    # Удаление связанных данных из travelplan_geo
    if hasattr(travel_plan, 'travelplan_geo'):
        travel_plan.travelplan_geo.delete()

    # Удаление картинки из папки media
    if travel_plan.image:
        image_path = os.path.join(settings.MEDIA_ROOT, travel_plan.image)
        if os.path.isfile(image_path):
            os.remove(image_path)
    try:
        travel_plan.delete()
        logger.info("План путешествия удалён: %s", travelplan_id)
    except Exception as e:
        logger.error("Ошибка при удалении плана путешествия: %s", e)
        raise
    messages.success(request, "План путешествия удален.")
    return HttpResponseRedirect(reverse('travel:get_travel_plan'))


@login_required
def travel_detail_full(request, travelplan_id):
    travel = get_object_or_404(travelplan, pk=travelplan_id)
    return render(request, 'travel_detail_full.html', {'travel': travel})


@login_required
def get_travel_plan_3D(request, travelplan_id):
    travel = get_object_or_404(travelplan, pk=travelplan_id)

    # Проверяем, принадлежит ли путешествие текущему пользователю
    if travel.user == request.user:
        pass
    elif travel.is_public:
        pass
    elif travel.friends_only:
        # Проверка на дружбу между текущим пользователем и владельцем путешествия
        friendship_exists = Friendship.objects.filter(
            (Q(user1=request.user) & Q(user2=travel.user)) |
            (Q(user1=travel.user) & Q(user2=request.user))
        ).exists()
        if not friendship_exists:
            return HttpResponse('У Вас нетдоступа к данному плану путешествия')
    else:
        return HttpResponse('У Вас нетдоступа к данному плану путешествия')
    
    # Проверяем, есть ли связанный travelplan_geo
    if hasattr(travel, 'travelplan_geo'):
       travelplan_geo_3D = travel.travelplan_geo

    # Обрабатываем данные GPX, если они имеются
    if travelplan_geo_3D.geojson:
        processed_gpx_data_3D = travelplan_geo_3D.geojson
        # преобразовываем время, если оно имеется в processed_gpx_data
        # if 'time_points' in processed_gpx_data:
        # processed_gpx_data['time_points'] = [convert_to_iso_format(time_str) for time_str in processed_gpx_data['time_points']]
    else:
        processed_gpx_data_3D = {}

    context = {
        'travel': travel,
        'gpx_data': json.dumps(processed_gpx_data_3D),
    }
    return render(request, '3Dmap.html', context)
