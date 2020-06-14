from django.shortcuts import reverse
from django.test import TestCase

from posts.models import Group, Post, User


class TestCreatePost(TestCase):
    def setUp(self):
        self.text = 'I\'m Muzzy! I\'m big Muzzy!'
        self.user = User.objects.create(username='muzzy')
        self.group = Group.objects.create(title='Gondoland', slug='gondoland')
        self.path = reverse('new_post')
        self.client.force_login(self.user)

    def test_newpost_auth_user_post_redirect_to_index(self):
        response = self.client.post(self.path, {'text': self.text})
        self.assertRedirects(response, reverse('index'))

    def test_newpost_with_text_added_to_model(self):
        self.client.post(self.path, {'text': self.text})
        self.assertTrue(Post.objects.filter(text=self.text).exists())

    def test_newpost_with_group_added_to_model(self):
        self.client.post(self.path, {
            'text': self.text, 'group': self.group.id})
        self.assertEqual(self.group.posts.last().text, self.text)

    def test_newpost_with_image_added_to_model(self):
        with open('posts/tests/image.png', 'rb') as img:
            self.client.post(self.path, {
                'text': self.text, 'image': img})
        self.assertTrue(Post.objects.first().image)

    def test_newpost_with_group_image_added_to_model(self):
        with open('posts/tests/image.png', 'rb') as img:
            self.client.post(self.path, {
                'text': self.text, 'group': self.group.id, 'image': img})
        self.assertTrue(self.group.posts.last().image)

    def test_newpost_form_error_with_nonimage(self):
        with open('posts/tests/nonimage.png', 'rb') as img:
            response = self.client.post(
                self.path,
                {'text': 'text', 'image': img},
            )
        self.assertIn('image', response.context['form'].errors)


class TestEditPost(TestCase):
    def setUp(self):
        self.text = 'I\'m Muzzy! I\'m big Muzzy!'
        self.new_text = 'I love parking meters'
        self.user = User.objects.create(username='muzzy')
        self.group1 = Group.objects.create(title='Gondoland', slug='gondoland')
        self.group2 = Group.objects.create(title='Neverland', slug='neverland')
        self.image_path = 'posts/photo.png'

        self.post = Post.objects.create(author=self.user,
                                        text=self.text,
                                        group=self.group1,
                                        image=self.image_path)

        self.path = reverse('post_edit',
                            kwargs={
                                'username': self.user.username,
                                'post_id': self.post.id})
        self.client.force_login(self.user)

    def test_editpost_auth_user_post_redirect_to_index(self):
        response = self.client.post(self.path, {'text': self.text})
        self.post = Post.objects.first()
        self.assertRedirects(response,
                             reverse('post_view',
                                     kwargs={
                                         'username': self.user.username,
                                         'post_id': self.post.id}))

    def test_editpost_text_changed(self):
        self.client.post(self.path, {'text': self.new_text})
        self.post = Post.objects.first()
        self.assertEqual(self.post.text, self.new_text)
        self.assertNotEqual(self.post.text, self.text)

    def test_editpost_group_changed(self):
        self.client.post(self.path, {
            'text': self.text, 'group': self.group2.id})
        self.post = Post.objects.first()
        self.assertEqual(self.post.group, self.group2)
        self.assertNotEqual(self.post.group, self.group1)
        self.assertEqual(self.group1.posts.count(), 0)
        self.assertEqual(self.group2.posts.count(), 1)

    def test_editpost_image_changed(self):
        with open('posts/tests/image.png', 'rb') as img:
            self.client.post(self.path, {
                'text': self.text, 'group': self.group1.id, 'image': img})
        self.post = Post.objects.first()
        self.assertEqual(self.post.text, self.text)
        self.assertEqual(self.post.group, self.group1)
        self.assertTrue(self.post.image)
        self.assertNotEqual(self.post.image, self.image_path)

    def test_editpost_image_remove(self):
        self.client.post(self.path, {
            'text': self.text, 'group': self.group1.id, 'image-clear': 'True'})
        self.post = Post.objects.first()
        self.assertEqual(self.post.text, self.text)
        self.assertEqual(self.post.group, self.group1)
        self.assertFalse(self.post.image)
        self.assertNotEqual(self.post.image, self.image_path)

    def test_editpost_group_remove(self):
        self.client.post(self.path, {'text': self.text, 'group': ''})
        self.post = Post.objects.first()
        self.assertFalse(self.post.group)
        self.assertNotEqual(self.post.group, self.group1)
        self.assertNotEqual(self.post.group, self.group2)
        self.assertEqual(self.group1.posts.count(), 0)
        self.assertEqual(self.group2.posts.count(), 0)

    def test_newpost_form_error_with_nonimage(self):
        with open('posts/tests/nonimage.png', 'rb') as img:
            response = self.client.post(
                self.path,
                {'text': 'text', 'image': img},
            )
        self.assertIn('image', response.context['form'].errors)


class TestGetPostInPages(TestCase):
    def setUp(self):
        self.text = 'I love parking meters'
        self.img_tag = 'img class="card-img" src="/media/'
        self.user = User.objects.create(username='muzzy')
        self.group = Group.objects.create(title='Gondoland', slug='gondoland')
        self.image_path = 'posts/photo.png'

        self.post = Post.objects.create(author=self.user,
                                        text=self.text,
                                        group=self.group,
                                        image=self.image_path)

        self.paths = (
            reverse('index'),
            reverse('profile', args=(self.user.username,)),
            reverse('group_posts', args=(self.group.slug,)),
            reverse('post_view', kwargs={
                'username': self.user.username, 'post_id': self.post.id
            }),
        )

    def test_get_newpost_text_at_paths(self):
        for path in self.paths:
            with self.subTest(path=path):
                self.assertContains(self.client.get(path), self.text)

    def test_get_newpost_image_at_paths(self):
        for path in self.paths:
            with self.subTest(path=path):
                self.assertContains(self.client.get(path), self.img_tag)
