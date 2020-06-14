from django.shortcuts import reverse
from django.test import TestCase

from posts.models import Comment, Post, User


class TestAddCommentCase(TestCase):
    def setUp(self):
        author = User.objects.create(username='alice')
        text = 'ALICE_MESSAGE'
        self.commentator = User.objects.create(username='corvex')
        self.comment = 'I like Alice'
        post = Post.objects.create(author=author, text=text)
        self.path = reverse('add_comment',
                            kwargs={
                                'username': post.author.username,
                                'post_id': post.id,
                            })

    def test_create_comment_through_form(self):
        self.client.force_login(self.commentator)
        self.client.post(self.path, {'text': self.comment})
        post = Post.objects.first()
        self.assertEqual(post.comments.last().text, self.comment)
        self.assertEqual(post.comments.count(), 1)
        self.assertEqual(post.comments.last().author, self.commentator)


class TestGetCommentInPage(TestCase):
    def setUp(self):
        user = User.objects.create(username='alice')
        text = 'ALICE_MESSAGE'
        post = Post.objects.create(author=user, text=text)
        self.comment = 'I like Bob'
        Comment.objects.create(author=user, post=post, text=self.comment)
        self.path = reverse('post_view',
                            kwargs={
                                'username': post.author.username,
                                'post_id': post.id,
                            })

    def test_get_comment_on_postpage(self):
        self.assertContains(self.client.get(self.path), self.comment)
