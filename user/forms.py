from django import forms
from .models import User, UserProfile


#Форма для модели пользователя
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

    password = forms.CharField(widget=forms.PasswordInput())    

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'usersurname', 'userage', 'usertype']

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    # Поля из модели User
    email = forms.EmailField()
    
    # Поля из модели UserProfile
    usertype = forms.CharField(max_length=50)
    usersurname = forms.CharField(max_length=70)
    username = forms.CharField(max_length=70)
    userage = forms.IntegerField(required=False)
    
    class Meta:
        model = User
        fields = ['email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        
        # Создаем объект UserProfile и связываем его с пользователем User
        user_profile = UserProfile(
            user=user,
            usertype=self.cleaned_data['usertype'],
            usersurname=self.cleaned_data['usersurname'],
            username=self.cleaned_data['username'],
            userage=self.cleaned_data['userage'],
        )

        if commit:
            if self.is_valid():
               user.save()
               user_profile.save()
        
        return user

