from django.shortcuts import reverse
from django.test import TestCase

from posts.models import Post, User


class TestGetPostUrlAndCode(TestCase):
    """
    Test avilable of url, and check of correcting return codes.
    """

    def setUp(self):
        self.user = User.objects.create(username='muzzy')
        self.post = Post.objects.create(text='Im big Muzzy', author=self.user)

    def test_get_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_get_profile_page(self):
        response = self.client.get(reverse('profile',
                                           args={self.user.username}))
        self.assertEqual(response.status_code, 200)

    def test_get_404_for_non_exist_url(self):
        # special wrong URL for test 404 code
        response = self.client.get('/some/url/with/error/')
        self.assertEqual(response.status_code, 404)

    def test_nonauth_user_redirect_code(self):
        response = self.client.get(reverse('new_post'))
        self.assertEqual(response.status_code, 302)

    def test_newpost_auth_user_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('new_post'))
        self.assertEqual(response.status_code, 200)

    def test_get_exist_post(self):
        response = self.client.get(reverse('post_view',
                                           kwargs={
                                               'username': self.user.username,
                                               'post_id': self.post.id,
                                           }))
        self.assertEqual(response.status_code, 200)

    def test_get_404_for_non_exist_post(self):
        response = self.client.get(reverse('post_view',
                                           kwargs={
                                               'username': self.user.username,
                                               'post_id': 31337,
                                           }))
        self.assertEqual(response.status_code, 404)


class TestFormExist(TestCase):
    """
    Test of existing forms and relevant fields.
    """

    def setUp(self):
        self.user = User.objects.create(username='Muzzy')
        self.post = Post.objects.create(text='Im big Muzzy', author=self.user)
        self.client.force_login(self.user)

    def test_form_newpost_existence(self):
        path = reverse('new_post')
        response = self.client.get(path)
        self.assertIn('form', response.context)

    def test_form_fields_newpost_existence(self):
        fields = ['text', 'group', 'image']
        path = reverse('new_post')
        response = self.client.get(path)

        for field in fields:
            self.assertIn(field, response.context['form'].fields)

    def test_form_editpost_existence(self):
        path = reverse('post_edit', kwargs={
            'username': self.user.username,
            'post_id': self.post.id
        })
        response = self.client.get(path)
        self.assertIn('form', response.context)

    def test_form_fields_editpost_existence(self):
        fields = ['text', 'group', 'image']
        path = reverse('post_edit', kwargs={
            'username': self.user.username,
            'post_id': self.post.id
        })
        response = self.client.get(path)

        for field in fields:
            self.assertIn(field, response.context['form'].fields)

    def test_form_comment_existence(self):
        path = reverse('post_view', kwargs={
            'username': self.user.username,
            'post_id': self.post.id
        })
        response = self.client.get(path)
        self.assertIn('form', response.context)

    def test_form_fields_comment_existence(self):
        path = reverse('post_view', kwargs={
            'username': self.user.username,
            'post_id': self.post.id
        })
        response = self.client.get(path)
        self.assertIn('text', response.context['form'].fields)
