from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем классы Bootstrap и плейсхолдеры к полям
        self.fields['username'].widget.attrs.update({
            'class': 'form-control w-100',
            'placeholder': 'Введите имя пользователя'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control w-100',
            'placeholder': 'Введите email'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control w-100',
            'placeholder': 'Введите пароль'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control w-100',
            'placeholder': 'Подтвердите пароль'
        })

        # Изменяем метки полей
        self.fields['username'].label = 'Имя пользователя'
        self.fields['email'].label = 'Email'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control w-100',
            'placeholder': 'Введите имя пользователя'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control w-100',
            'placeholder': 'Введите пароль'
        }) 