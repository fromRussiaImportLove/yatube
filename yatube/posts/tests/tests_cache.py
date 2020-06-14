from django.core.cache import cache
from django.shortcuts import reverse
from django.test import TestCase, override_settings

from posts.models import Post, User


class TestCachingPost(TestCase):
    def setUp(self):
        self.text = 'I love parking meters'
        self.user = User.objects.create(username='muzzy')
        self.post = Post.objects.create(author=self.user,
                                        text=self.text,)
        self.paths = (
            reverse('index'),
            reverse('profile', args=(self.user.username,)),
        )
        cache.clear()

    @override_settings(
        CACHES={
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            }
        }
    )
    def test_caching_text(self):
        cache.clear()
        self.assertContains(self.client.get(reverse('index')), self.text)
        self.post.text = 'SOME_ANOTHER_TEXT'
        self.post.save()
        self.assertContains(self.client.get(reverse('index')), self.text)

    def test_new_post_is_on_index(self):
        text = 'SOME_ANOTHER_TEXT'
        cache.clear()
        with self.settings(CACHES={
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}):
            self.client.get(reverse('index'))
            self.client.force_login(self.user)
            self.client.post(reverse('new_post'), {'text': text}, follow=True)
            response_index = self.client.get(reverse('index'))
            self.assertNotContains(response_index, text)

    def test_header(self):
        response = self.client.get(reverse('index'))
        self.assertTrue(response.has_header('Cache-Control'))
