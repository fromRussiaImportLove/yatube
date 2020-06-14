from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()

    def __str__(self):
        return f'{self.slug}: {self.title}'


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        verbose_name='date published',
        auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts')
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts')
    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return f'{self.pub_date.date()} {self.text[:15]} ({self.pk})'


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        verbose_name='date commented',
        auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.author.username} {self.text[:15]} ({self.pk})'


class FollowManager(models.Manager):
    def is_follow(self, author, user):
        if user.is_authenticated:
            return super().filter(author=author, user=user).exists()
        return False

    def posts(self):
        authors = self.all().values('author_id')
        posts_list = Post.objects.filter(
            author__in=authors).order_by('-pub_date')
        return posts_list

    def check_related_name(self, user_obj):
        """
        Расставляем автора и пользователя в зависимости от realted_name 
        Дополнительная функция, которая в зависимости от отношений
        (соответствующего сета) понимает кто есть автор, а кто пользователь
        сделана для универсальности вызова функций contains, append, remove
        """
        user, author = self.instance, user_obj
        if self.field.name == 'author':
            user, author = author, user
        return user, author

    def contains(self, user_obj):
        """ 
        Универсальный метод для проверки followers и following 

        Одинаково корректно проверят вне зависимости от related_name.
        Можно использовать как user.follower.contains(author)
        Чтобы проверить есть ли автор в подписках пользователя
        И можно наоборот author.following.contains(user)
        Чтобы проверить есть ли пользователь в последователях у автора.

        :param user_obj: в зависимости от контекста user или author
        """
        user, author = self.check_related_name(user_obj)
        return self.is_follow(author=author, user=user)

    def append(self, user_obj):
        """
        Универасальный метод добавить как любимого автора так и подписчика
        Вызывается подобно contains:
        user.follower.append(author)
        author.following.append(user)
        """
        user, author = self.check_related_name(user_obj)
        if author != user:
            self.get_or_create(user=user, author=author)

    def remove(self, user_obj):
        """ Универсальный метод по удалению любимого автора или подписчика """
        user, author = self.check_related_name(user_obj)
        follow = self.filter(user=user, author=author)
        follow.delete()

    def switch(self, user_obj):
        """ Метод который позволят переключать состояние: подписан/нет """
        if self.contains(user_obj):
            self.remove(user_obj)
        else:
            self.append(user_obj)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following')

    objects = FollowManager()

    class Meta:
        models.UniqueConstraint(fields=['user', 'author'],
                                name='unique_follow')

    def __str__(self):
        return f'{self.user.username} follow to {self.author.username}'
