from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем классы Bootstrap и плейсхолдеры к полям
        self.fields['title'].widget.attrs.update({
            'class': 'form-control w-100',
            'placeholder': 'Введите заголовок поста'
        })
        self.fields['content'].widget.attrs.update({
            'class': 'form-control w-100',
            'placeholder': 'Введите содержание поста',
            'rows': '6'
        })
        self.fields['category'].widget.attrs.update({
            'class': 'form-control w-100'
        })
        self.fields['image'].widget.attrs.update({
            'class': 'form-control w-100'
        })

        # Изменяем метки полей
        self.fields['title'].label = 'Заголовок'
        self.fields['content'].label = 'Содержание'
        self.fields['category'].label = 'Категория'
        self.fields['image'].label = 'Изображение (необязательно)'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control w-100',
                'rows': '3',
                'placeholder': 'Напишите ваш комментарий...'
            })
        }
        labels = {
            'content': 'Комментарий'
        } 