from django.shortcuts import reverse
from django.test import TestCase

from posts.models import Post, User


class TestAuthUrl(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='Muzzy')
        self.post = Post.objects.create(text='text', author=self.user)
        self.path_kwargs = {
            'username': self.user.username,
            'post_id': self.post.id
        }

    def test_nonauth_user_redirect_to_auth_page(self):
        paths = (
            reverse('new_post'),
            reverse('follow_index'),
            reverse('post_edit', kwargs=self.path_kwargs),
            reverse('add_comment', kwargs=self.path_kwargs),
            reverse('profile_follow', kwargs={'username': self.user.username}),
            reverse('profile_unfollow', args={self.user.username}),
        )

        login_path = reverse('login')

        for path in paths:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertRedirects(
                    response,
                    login_path+'?next='+path,
                    status_code=302
                )
