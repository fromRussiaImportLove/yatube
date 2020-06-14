from django.forms import ModelForm, Textarea

from posts.models import Comment, Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'text', 'image')
        labels = {
            'group': 'Тематическая группа',
            'text': 'Ваша заметка',
            'image': 'Изображение',
        }
        help_texts = {
            'group': 'Ваш пост появиться в этой группе',
            'text:': 'Здесь вы можете излить свои мысли',
            'image': 'Иллюстрация добавит выразительности',
        }
        widgets = {
            'text': Textarea(attrs={
                'placeholder': 'Здесь вы можете излить свои мысли',
                'overflow': 'auto',
            }),
        }
        error_messages = {
            'image': {
                'images': 'нужна каринка',
                'invalid_extension': 'картинка нужна',
            },
            'text': {
                'required': 'без гениальных мыслей нельзя',
            }
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            'text': 'текст комментария',
        }
        help_texts = {
            'text': 'можно добавить остроты',
        }
        error_messages = {
            'text': {
                'required': 'без гениальных мыслей нельзя',
            },
        }
        widgets = {
            'text': Textarea(attrs={
                'width': '90%',
                'rows': 4,
                'resize': 'vertical',
                'PlaceHolder': 'Писать тут', }),
        }
