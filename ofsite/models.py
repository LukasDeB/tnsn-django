from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.utils import timezone

from django.db import models
from django import forms

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, related_name='user_profile', null=True)
    msg = models.TextField()

class Comments(models.Model):
    author = models.ForeignKey(User, related_name='comment_author')
    content = models.TextField()



class Posts(models.Model):
    author = models.ForeignKey(User, related_name='post_author')
    content = models.TextField()
    comments = models.ForeignKey(Comments, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def get_comments(self):
        qs = Comments.objects.filter(pk__in=self.comments)
        c = []
        for com in qs:
            c.append(com)
        return c

class FriendRequest(models.Model):

    from_user = models.ForeignKey(User, related_name="request_from")
    to_user = models.ForeignKey(User, related_name="request_to")
    message = models.CharField(max_length=200, blank=True)
    accepted = models.BooleanField(default=False)

    def accept(self):
        Friend.objects.get(user=self.from_user).friends.add(Friend.objects.get(user=self.to_user))
        self.accepted = True
        self.delete()

    def decline(self):
        self.delete()

    def cancel(self):
        self.delete()


class FriendshipManager(models.Manager):

    def friends(self, user):
        qs = User.objects.filter(friendship__friends__user=user)
        friends = qs.order_by('?')
        return friends

    def are_friends(self, user1, user2):
        qs = Friend.objects.get(user=user1).friends.filter(user=user2).exists()
        return bool(qs)

    def requests_sent(self,user):
        qs = FriendRequest.objects.filter(from_user=user)
        return qs

    def requests_received(self,user):
        qs = FriendRequest.objects.filter(to_user=user)
        return qs


class Friend(models.Model):
    user = models.OneToOneField(User, related_name='friendship', null=True)
    friends = models.ManyToManyField('self', symmetrical=True)

    created = models.DateTimeField(default=timezone.now)

    objects = FriendshipManager()
