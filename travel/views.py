from django.shortcuts import render, redirect, get_object_or_404
from .form import TravelPlanformTrue, PointTrekForm, TravelDescriptionForm
from .models import travelplan, traveltype, Friendship, travelplan_geo, plpoint_trek, point_trek, description, travelplandescription
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
from django import forms
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import subprocess
import shutil
from django.core.files.storage import FileSystemStorage

logger = logging.getLogger(__name__)

@login_required
def create_travel_plan(request):
    # Создание путешевствия по треку существующему
    form = TravelPlanformTrue()
    # Если форма отправлена методом POST, то мы создаем экземпляр формы  с данными
    if request.method == 'POST':

        form = TravelPlanformTrue(request.POST, request.FILES)

        # Если форма валидна, сохраняем данные в базу данных
        if form.is_valid():
            # Создаем экземпляр модели travelplan с данными из формы
            travel_plan = form.save(commit=False)

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

            # Получаем файл JPG из формы
            image_file = request.FILES.get('image')
            if image_file:
                if not image_file.name.endswith('.jpg'):
                    messages.error(
                        request, "Неверный формат файла. Пожалуйста, загрузите jpg файл.")
                    # Удаляем только что созданный travel_plan, так как процесс создания не завершен
                    travel_plan.delete()
                    return render(request, 'create_travel_plan.html', {'form': form, 'traveltypes': traveltype.objects.all()})
                try:
                    # Сохраняем изображение в папку
                    image_path = import_imge(image_file, travel_plan.travelplan_id)
                    travel_plan.image = image_path
                    travel_plan.save()  # Обновляем объект с изображением
                    # Дальнейшая обработка
                except Exception as e:
                    # Обработка исключения
                    messages.error(request, "Произошла ошибка при обработке jpg файла: {}".format(e))
                    travel_plan.delete()  # Удаляем только что созданный travel_plan
                    return render(request, 'create_travel_plan.html', {'form': form, 'traveltypes': traveltype.objects.all()})
                
            messages.success(request, "Путешевствие создано успешно!")
            return redirect('travel:get_travel_plan')

    else:
        # Если форма не отправлена методом POST, создаем пустую форму
        print(form.errors)
        form = TravelPlanformTrue()
    # Отображаем шаблон с формой, передавая форму в контексте
    return render(request, 'create_travel_plan.html', {'form': form, 'traveltypes': traveltype.objects.all()})

def import_imge(file, travelplan_id, output_size=(400, 267)):
    # Импорт изображений для карточки путешевствия
    if file is None:
        return None
    try:
        # Путь и имя файла для сохранения
        folder_name = os.path.join('travelfoto', str(travelplan_id))  # Папка с ID путешествия
        file_name = os.path.join(folder_name, file.name)
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

        media_url = os.path.join(settings.MEDIA_URL, file_name).replace('\\', '/')

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
def get_travel_plan(request):
    # Страница с карточками путешевствий
    current_user = request.user

    # Получение данных только для текущего пользователя
    travel = travelplan.objects.filter(user=current_user)

    return render(request, 'get_travel_plan.html', {'travel': travel})

@login_required
def travel_detail_chart(request, travelplan_id):
    # Функция передает данные для графиков, и карт, точек маршрута, точек трека
    current_user = request.user

    # Получение плана путешествия и проверка доступа
    travel_plan = get_object_or_404(travelplan, pk=travelplan_id)    
    if travel_plan.user != current_user and not travel_plan.is_public and not (
        travel_plan.friends_only and Friendship.objects.filter(
            (Q(user1=current_user) & Q(user2=travel_plan.user)) |
            (Q(user1=travel_plan.user) & Q(user2=current_user))
        ).exists()):
        return HttpResponse('У Вас нет доступа к данному плану путешествия')
    
    # Получение связанных точек путешествия
    travel_points = plpoint_trek.objects.filter(travelplan=travel_plan).select_related('point_trek')
    points = [tp.point_trek for tp in travel_points]  
  
    # Обрабатываем данные GPX_point, если они имеются
    gpx_data_point = {}
    for point in points:
        if point.point_сoordinates:
            gpx_data_point[point.point_trek_id] = point.point_сoordinates

        # Проверяем, есть ли связанный travelplan_geo
    if hasattr(travel_plan, 'travelplan_geo'):
       travelplan_geo_instance = travel_plan.travelplan_geo

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
        'travel': travel_plan,
        'travel_points': points,
        'gpx_data': json.dumps(processed_gpx_data),
        'gpx_data_track': json.dumps(track_coordinates),
        'gpx_data_point': json.dumps(gpx_data_point),
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
@require_POST
def delete_travel_plan(request, travelplan_id):
    # Удаление планов путешевствий
    logger.info("Запрос на удаление плана путешествия с ID: %s", travelplan_id)

    travel_plan = get_object_or_404(travelplan, pk=travelplan_id, user=request.user)

    # Удаление связанных данных из travelplan_geo
    if hasattr(travel_plan, 'travelplan_geo'):
        travel_plan.travelplan_geo.delete()

    # Удаление картинки из папки media
    folder_path = os.path.join(settings.MEDIA_ROOT, 'travelfoto', str(travelplan_id))
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        shutil.rmtree(folder_path)

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
    # Функция для передачи деталей путешевствия в шаблон
    travel = get_object_or_404(travelplan, pk=travelplan_id)
    return render(request, 'travel_detail_full.html', {'travel': travel})

@login_required
def get_travel_plan_3D(request, travelplan_id):
    # 3D картав путешевствии
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

@login_required
def add_point_trek(request, travelplan_id):
    # Обработка формы для записи точек путешеввствий в БД
    travel = get_object_or_404(travelplan, pk=travelplan_id)
    if request.method == 'POST':
        point_form = PointTrekForm(request.POST)
        if point_form.is_valid():
            point = point_form.save(commit=False)

            # Данные в формате GeoJSON из очищенных данных формы
            geojson_data = point_form.cleaned_data['point_сoordinates']

            # Присваиваем GeoJSON данные полю point_coordinates
            point.point_сoordinates = geojson_data

            point.save()  # Сохраняем объект в БД

            # Создание связующей записи
            plpoint_trek.objects.create(travelplan=travel, point_trek=point)

            # Редирект на страницу деталей путешествия
            return redirect('travel:travel_detail_chart', travelplan_id=travelplan_id)
    else:
        point_form = PointTrekForm()

    return render(request, 'travel_detail_chart.html', {'form': point_form, 'travel': travel})

@login_required
@require_POST
def delete_travel_point(request, point_trek_id):
    # Удаление планов путешевствий
    logger.info("Запрос на удаление точек путешествия с ID: %s", point_trek_id)

    travel_point = get_object_or_404(point_trek, pk=point_trek_id)

    # Получаем travelplan_id перед удалением
    travelplan_id = travel_point.plpoint_trek_set.first().travelplan_id
    
    # Удаляем саму точку путешествия
    travel_point.delete()

    return HttpResponseRedirect(reverse('travel:travel_detail_chart', args=[travelplan_id]))

@login_required
@require_POST
def upload_video(request):
    video = request.FILES.get('video')
    if not video:
        return JsonResponse({'status': 'error', 'message': 'No video file provided'}, status=400)
    try:
        # Генерация уникального имени файла
        file_name = default_storage.save(os.path.join('video', video.name), ContentFile(video.read()))
        file_url = default_storage.url(file_name)
        return JsonResponse({'status': 'success', 'url': file_url})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
@login_required
def travel_description(request, travelplan_id):
    # Функция для передачи деталей путешевствия в шаблон
    travel = get_object_or_404(travelplan, pk=travelplan_id)    

    # Получаем все связанные объекты description для данного travelplan
    descriptions = travelplandescription.objects.filter(travelplan=travel).select_related('description')

    form = TravelDescriptionForm()  # Создайте экземпляр формы

    # Собираем все фотографии и описания
    photos = []
    for item in descriptions:
        for i in range(1, 11):
            image_field = f'media_{i}'
            desc_field = f'description_media_{i}'
            image_url = getattr(item.description, image_field, None)
            description = getattr(item.description, desc_field, '')
            if image_url:
                photos.append({'image_url': image_url, 'description': description})


    return render(request, 'travel_description.html', {'travel': travel, 'photos': photos, 'form': form})

@login_required
@require_POST
def add_media_travel(request, travelplan_id):
    name_descriptiond = request.POST.get('namepoint')
    image_file = request.FILES.get('image')
    print(name_descriptiond)

    # Получаем объект travelplan
    travel = get_object_or_404(travelplan, pk=travelplan_id)

    try:
        # Обработка и сжатие изображения
        output_size = (1280, 720)  # Новый размер изображения
        folder_name = os.path.join('travelfoto', str(travelplan_id))
        file_name = os.path.join(folder_name, image_file.name)
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        # Создаем директорию, если она не существует
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Открываем файл изображения с помощью Pillow
        image = Image.open(image_file)

        # Меняем размер и сохраняем
        image = image.resize(output_size, Image.Resampling.LANCZOS)
        image.save(file_path, image.format, quality=85, optimize=True)
        uploaded_file_url = os.path.join(settings.MEDIA_URL, file_name).replace('\\', '/')
    except IOError:
        print("Ошибка при обработке изображения")
        return None  

    # Поиск существующего объекта description или создание нового
    travelplandescription_obj = travelplandescription.objects.filter(travelplan=travel).first()
    if travelplandescription_obj:
        description_obj = travelplandescription_obj.description
    else:
        description_obj = description()
        description_obj.save()
        travelplandescription_obj = travelplandescription.objects.create(
            travelplan=travel,
            description=description_obj
        )
    
    # Проверка, не превышено ли максимальное количество изображений
    image_fields = [f'media_{i}' for i in range(1, 11)]
    existing_images = [getattr(description_obj, field) for field in image_fields if getattr(description_obj, field)]
    if len(existing_images) >= 10:
        # Отправляем сообщение об ошибке, если количество изображений превысило 10
        messages.error(request, "Вы уже загрузили максимальное количество изображений.")
        return HttpResponseRedirect(reverse('travel:travel_description', kwargs={'travelplan_id': travelplan_id}))
    
    # Добавляем новое изображение в первое свободное поле
    for field in image_fields:
        if not getattr(description_obj, field):
            setattr(description_obj, field, uploaded_file_url)
            setattr(description_obj, f'description_{field}', name_descriptiond)
            description_obj.save()
            break

    return HttpResponseRedirect(reverse('travel:travel_description', kwargs={'travelplan_id': travelplan_id}))