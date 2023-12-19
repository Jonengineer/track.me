from django import forms
from .models import (travelplan, 
                     traveltype, 
                     point_trek, 
                     description, 
                     expense, 
                     track_map)
import json
from PIL import Image
from django.conf import settings
import os
from django.core.exceptions import ValidationError


class TravelPlanformTrue(forms.ModelForm):
    # Создание путешевствий
    class Meta:
        model = travelplan
        fields = ['country', 'territory', 'datestart', 'datefinish', 'traveltype', 'gpxtrek']
    gpxtrek = forms.FileField(required=False, label='GPX Trek (GPX)',
                              widget=forms.FileInput(attrs={'accept': '.gpx'}))
    
    traveltype = forms.ModelChoiceField(queryset=traveltype.objects.all(), empty_label=None)

    image = forms.ImageField(required=False, label='Изображение (JPG)', 
                            widget=forms.FileInput(attrs={'accept':'image/jpeg'}))

class PointTrekForm(forms.ModelForm):
    # Добавляем кастомное поле для координат
    point_сoordinates = forms.CharField(label='point_сoordinates', required=True)

    class Meta:
        model = point_trek
        fields = ['namepoint', 'description', 'point_сoordinates']  # Обновляем список полей

    def clean_point_сoordinates(self):
        coordinates_str = self.cleaned_data['point_сoordinates']
        namepoint = self.cleaned_data['namepoint']

        try:
            lat, lng = map(float, coordinates_str.split(', '))
            geojson_data = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lng, lat]
                },
                "properties": {
                    "name": namepoint  # Здесь вы можете установить имя, если это необходимо
                }
            }
           
            return geojson_data
        except ValueError:
            raise forms.ValidationError('Invalid coordinates format. Please use "latitude, longitude."')
        
class TravelDescriptionForm(forms.ModelForm):

    class Meta:
        model = description
        fields = ['title_descriptiond', 'name_descriptiond']  # Обновляем список полей
        widgets = {
            'title_descriptiond': forms.Textarea(attrs={'class': 'materialize-textarea', 'id': 'textarea3', 'data-length': '100', 'placeholder': 'Добавьте заголовок'}),
            'name_descriptiond': forms.Textarea(attrs={'class': 'materialize-textarea', 'id': 'textarea4', 'data-length': '6000', 'placeholder': 'Добавьте описание'}),
        }
        
class TravelFinanceForm(forms.ModelForm):    
    
    class Meta:
        model = expense
        fields = ['amount', 'nameexpense', 'quantity_day', 'quantity_people']  # Обновите список полей
        widgets = {            
            'amount': forms.NumberInput(attrs={
                'class': 'input-point', 
                'id': 'input_amount', 
                'step': '0.01',  # Шаг для числовых значений                
            }),
            'nameexpense': forms.TextInput(attrs={
                'class': 'input-point', 
                'id': 'input_nameexpense', 
                'data-length': '100'
            }),
            'quantity_day': forms.NumberInput(attrs={
            'class': 'input-point', 
            'id': 'input_quantity_day', 
            'step': '1',               
            }),
            'quantity_people': forms.NumberInput(attrs={
                'class': 'input-point', 
                'id': 'input_quantity_people', 
                'step': '1',              
            }),
        }    
    
class TrekForm(forms.ModelForm):
    # Добавляем кастомные поля для 10 координат точек
    for i in range(1, 11):
        locals()[f'point_{i}_coordinates'] = forms.CharField(
            label=f'Point {i} Coordinates', 
            required=False
        )

    class Meta:
        model = track_map
        fields = ['track_coordinat', 'gpxtrek']  # Включаем основные поля модели

    def clean(self):
        cleaned_data = super().clean()

        # Создаем список для хранения координат
        coordinates_list = []

        for i in range(1, 11):
            coordinates_str = cleaned_data.get(f'point_{i}_coordinates')
            if coordinates_str:
                try:
                    lat, lng = map(float, coordinates_str.split(', '))
                    coordinates_list.append({'lat': lat, 'lng': lng})
                except ValueError:
                    self.add_error(f'point_{i}_coordinates', 'Invalid coordinates format. Please use "latitude, longitude".')

        # Проверяем, что хотя бы одна точка заполнена
        if not coordinates_list:
            raise ValidationError("At least one point is required.")

        # Добавляем список координат в очищенные данные
        cleaned_data['coordinates_list'] = coordinates_list
        return cleaned_data
