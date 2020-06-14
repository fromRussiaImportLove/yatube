from django.shortcuts import reverse
from django.test import TestCase

from posts.models import User


class TestSignUpUser(TestCase):
    def setUp(self):
        first_name = 'testusername_first_name'
        last_name = 'testusername_last_name'
        username = 'testusername'
        password = '321asdas'
        self.data = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'password1': password,
            'password2': password
        }

    def test_sign_up_success(self):
        signup_url = reverse('signup')
        login_url = reverse('login')
        response = self.client.post(signup_url, self.data)
        self.assertRedirects(
            response, login_url, status_code=302, target_status_code=200)
        user_cnt = User.objects.all().count()
        self.assertEqual(user_cnt, 1, 'Пользователь не создан')

    def test_sign_up_fail_with_diff_passwords(self):
        self.data['password2'] = 'another_password'
        signup_url = reverse('signup')
        response = self.client.post(signup_url, self.data)
        self.assertTrue(response.context_data['form'].errors)


class TestProfilePage(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='Muzzy')

    def test_get_404_for_profile_non_exist_user(self):
        response = self.client.get(reverse('profile',
                                           args={'non-exist-username'}))
        self.assertEqual(response.status_code, 404)

    def test_get_profile_page(self):
        response = self.client.get(reverse('profile',
                                           args={self.user.username}))
        self.assertEqual(response.status_code, 200)
