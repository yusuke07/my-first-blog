from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    def __str__(self):
        return self.username + ":" + self.email


class Post(models.Model):
    """投稿モデル"""
    class Meta:
        db_table = 'post'

    No = models.CharField(verbose_name='ID', max_length=255, blank=True)
    Score = models.CharField(verbose_name='スコア', max_length=255, default='', blank=True)
    TOEIC = models.CharField(verbose_name='TOEIC', max_length=255, blank=True)
    Sex = models.CharField(verbose_name='性別', max_length=255, default='', blank=True)
    Date = models.CharField(verbose_name='生年月日', max_length=255, blank=True)
    Sentence = models.CharField(verbose_name='発話', max_length=255, default='', blank=True)
    #author = models.ForeignKey(
        #'search.CustomUser',
        #on_delete=models.CASCADE,
        #related_name='posts',
    #)
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return self.No

    @staticmethod
    def get_absolute_url(self):
        return reverse('search:index')