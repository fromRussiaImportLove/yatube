from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CreationForm(UserCreationForm):
    """
    Собственный классы для формы регистрации.
    Наследуем не от кастомных модей, а от встроенного UserCrationForm
    В качестве модели используем встроенную User
    """

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
