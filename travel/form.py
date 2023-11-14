from django import forms
from .models import travelplan, traveltype


class TravelPlanformTrue(forms.ModelForm):
    # Создание путешевствий
    class Meta:
        model = travelplan
        fields = ['country', 'territory', 'datestart', 'datefinish', 'description', 'traveltype', 'gpxtrek']
    gpxtrek = forms.FileField(required=False, label='GPX Trek (GPX)',
                              widget=forms.FileInput(attrs={'accept': '.gpx'}))
    
    traveltype = forms.ModelChoiceField(queryset=traveltype.objects.all(), empty_label=None)

    image = forms.ImageField(required=False, label='Изображение (JPG)', 
                            widget=forms.FileInput(attrs={'accept':'image/jpeg'}))
