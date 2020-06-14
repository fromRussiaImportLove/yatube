from django.shortcuts import reverse
from django.test import TestCase

from posts.models import Follow, Post, User


class TestFollowingCase(TestCase):
    def setUp(self):
        self.alice = User.objects.create(username='alice')
        self.bob = User.objects.create(username='bob')
        self.corvex = User.objects.create(username='corvex')
        Follow.objects.create(user=self.bob, author=self.alice)
        self.text = 'ALICE_MESSAGE'

    def test_follow_author(self):
        self.client.force_login(self.alice)
        self.client.get(reverse('profile_follow',
                                args={self.bob.username}))
        self.assertEqual(self.alice.follower.count(), 1)

    def test_unfollow_author(self):
        self.client.force_login(self.bob)
        self.client.get(reverse('profile_unfollow',
                                args={self.alice.username}))
        self.assertEqual(self.bob.follower.count(), 0)

    def test_newpost_in_following(self):
        Post.objects.create(author=self.alice, text=self.text)
        self.client.force_login(self.bob)
        response = self.client.get(reverse('follow_index'))
        self.assertContains(response, self.text)

    def test_newpost_not_in_unfollowing(self):
        Post.objects.create(author=self.alice, text=self.text)
        self.client.force_login(self.corvex)
        response = self.client.get(reverse('follow_index'))
        self.assertNotContains(response, self.text)

    def test_hidepost_after_unfollowing(self):
        Post.objects.create(author=self.alice, text=self.text)
        self.client.force_login(self.bob)
        self.client.get(reverse('profile_unfollow',
                                args={self.alice.username}))
        response = self.client.get(reverse('follow_index'))
        self.assertNotContains(response, self.text)

    def test_double_unfollow_author(self):
        self.client.force_login(self.alice)
        self.client.get(reverse('profile_unfollow',
                                args={self.bob.username}))
        self.assertEqual(self.alice.follower.count(), 0)

    def test_double_follow_author(self):
        self.client.force_login(self.bob)
        self.client.get(reverse('profile_follow',
                                args={self.alice.username}))
        self.assertEqual(self.bob.follower.count(), 1)

    def test_cant_follow_userself(self):
        self.client.force_login(self.corvex)
        self.client.get(reverse('profile_follow',
                                args={self.corvex.username}))
        self.assertEqual(self.corvex.follower.count(), 0)
