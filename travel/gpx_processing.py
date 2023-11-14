import xml.etree.cElementTree as ET
from geopy.distance import geodesic
from datetime import datetime, timedelta

def is_significant_change(current_point, previous_point, time_threshold=2000, distance_threshold=500, elevation_threshold=50):
    """
    Определение, является ли изменение значимым.
    time_threshold - в секундах
    distance_threshold - в метрах
    elevation_threshold - в метрах
    """
    lat, lon, ele, time = current_point
    prev_lat, prev_lon, prev_ele, prev_time = previous_point

    # Проверяем, превышают ли различия пороговые значения
    time_diff = (time - prev_time).total_seconds()
    distance = geodesic((prev_lat, prev_lon), (lat, lon)).meters
    elevation_diff = abs(ele - prev_ele)

    return (time_diff > time_threshold) or (distance > distance_threshold) or (elevation_diff > elevation_threshold)


def parse_gpx_data(gpx_data):
    root = ET.fromstring(gpx_data)

    # Общие списки точек
    time_points = []
    elevation_points = []
    distances = []
    heart_rate_points = []
    speeds = []

    # Переменные для расчета статистики
    total_distance = 0
    moving_time = timedelta(0)
    total_ascent = 0
    total_descent = 0
    previous_point = None
    max_speed = 0

    # Создание GeoJSON структуры
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    
    # Создание списка координат для GeoJSON
    coordinates = []

    for trkpt in root.findall(".//{http://www.topografix.com/GPX/1/1}trkpt"):
        lat = float(trkpt.attrib['lat'])
        lon = float(trkpt.attrib['lon'])
        ele = float(trkpt.find("{http://www.topografix.com/GPX/1/1}ele").text)
        time_string = trkpt.find("{http://www.topografix.com/GPX/1/1}time").text
        time = datetime.fromisoformat(time_string.rstrip("Z"))

        # Извлекаем данные о пульсе, если они есть
        hr_element = trkpt.find(".//{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}hr")
        hr = int(hr_element.text) if hr_element is not None else None

        current_point = (lat, lon, ele, time)
        
        # Добавляем точки в списки
        time_points.append(time)
        elevation_points.append(ele)
        heart_rate_points.append(hr)
        
        coordinates.append([float(lon), float(lat), ele])

        # Вычисляем дистанцию и скорость
        if previous_point and not is_significant_change(current_point, previous_point):
            # Рассчитываем дистанцию и скорость для текущего участка
            distance = geodesic(previous_point[:2], (lat, lon)).meters
            time_difference = (time - previous_point[3]).total_seconds()
            speed = (distance / time_difference) * 3.6 if time_difference else 0
            speeds.append(speed)

            # Обновляем общие данные
            total_distance += distance
            distances.append(total_distance)
            max_speed = max(max_speed, speed)

            # Если расстояние между точками больше 1 метра, считаем, что объект в движении
            if distance > 2.7:
                moving_time += timedelta(seconds=time_difference)

            # Обновляем данные о подъеме и спуске
            elevation_diff = ele - elevation_points[-2]
            if elevation_diff > 0:
                total_ascent += elevation_diff
            elif elevation_diff < 0:
                total_descent += abs(elevation_diff)
        # Если предыдущая точка существует, но было обнаружено значительное изменение
        elif previous_point and is_significant_change(current_point, previous_point):
        # Мы не добавляем данные от аномального участка
        # Но мы не сбрасываем накопленные данные статистики
            pass  # Просто пропускаем текущий сегмент

        # Запоминаем текущую точку как предыдущую для следующего сравнения
        previous_point = current_point

    # Вычисляем общие статистики
    total_time = (time_points[-1] - time_points[0]).total_seconds() if time_points else 0
    moving_time_seconds = moving_time.total_seconds()
    total_distance_travelled = distances[-1] if distances else 0

    # Средняя скорость и скорость в движении
    speed_middle = (total_distance_travelled / total_time) * 3.6 if total_time else 0
    speed_moving = (total_distance_travelled / moving_time_seconds) * 3.6 if moving_time_seconds else 0


    # После цикла добавляем Feature для LineString в GeoJSON
    feature = {
        "type": "Feature",
        "properties": {
            # Добавьте другие свойства здесь, если необходимо
        },
        "geometry": {
            "type": "LineString",
            "coordinates": coordinates
        }
    }
    # Добавляем данные в итоговый словарь
    geojson['features'].append(feature)

    context = {
        'time_points': time_points,
        'elevation_points': elevation_points,
        'heart_rate_points': heart_rate_points,
        'distances': distances,
        'total_distance_travelled': total_distance_travelled,
        'total_time_seconds': total_time,
        'moving_time_seconds': moving_time_seconds,
        'speed_middle': speed_middle,
        'speed_moving': speed_moving,
        'total_ascent': total_ascent,
        'total_descent': total_descent,
        'max_speed': max_speed,
        'geojson': geojson,
    }

    return context
