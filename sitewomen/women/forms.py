from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from .models import Women


class AddPostForm(forms.ModelForm):
    """Класс формы для добавления поста
    Args:
        forms (class): _description_
    """

    def __init__(self, *args, **kwargs):
        """Конструктор формы для добавления поста"""
        super().__init__(*args, **kwargs)
        self.fields["cat"].empty_label = "Категория не выбрана"
        self.fields["husband"].empty_label = "Не замужем"

    class Meta:
        """Метаданные для формы добавления поста"""

        model = Women
        fields = [
            "title",
            "slug",
            "content",
            "photo",
            "is_published",
            "cat",
            "husband",
            "tags",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "content": forms.Textarea(attrs={"cols": 50, "rows": 5}),
        }

    def clean_title(self):
        """Собственный валидатор для поля title, который проверяет наличия
        загруженного поста, не позволял вводить строку более 50 символов
        """
        title = self.cleaned_data["title"]
        if len(title) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return title


class RegisterUserForm(UserCreationForm):
    """Класс формы для регистрации пользователя
    Args:
        UserCreationForm (class): _description_
    """

    username = forms.CharField(
        label="Логин", widget=forms.TextInput(attrs={"class": "form-input"})
    )
    first_name = forms.CharField(
        label="Имя", widget=forms.TextInput(attrs={"class": "form-input"})
    )
    last_name = forms.CharField(
        label="Фамилия", widget=forms.TextInput(attrs={"class": "form-input"})
    )
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-input"})
    )
    password1 = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-input"})
    )
    password2 = forms.CharField(
        label="Повтор пароля", widget=forms.PasswordInput(attrs={"class": "form-input"})
    )
    captcha = CaptchaField(label="Введите ответ")

    class Meta:
        """Метаданные для формы регистрации пользователя"""

        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class LoginUserForm(AuthenticationForm):
    """Класс формы для авторизации пользователя
    Args:
        AuthenticationForm (class): _description_
    """

    username = forms.CharField(
        label="Логин", widget=forms.TextInput(attrs={"class": "form-input"})
    )
    password = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-input"})
    )
    captcha = CaptchaField(label="Введите ответ")


class ContactForm(forms.Form):
    """Класс формы для отправки сообщения
    Args:
        forms (class): _description_
    """

    name = forms.CharField(label="Имя", max_length=255)
    email = forms.EmailField(label="Email")
    content = forms.CharField(
        label="Содержание", widget=forms.Textarea(attrs={"cols": 60, "rows": 10})
    )
    captcha = CaptchaField(label="Введите ответ")


# class UploadFileForm(forms.Form):
#     file = forms.ImageField(label="Изображение")