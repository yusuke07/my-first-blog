from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Post
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class SearchForm(forms.Form):

    Sentence = forms.CharField(
        initial='',
        label='発話',
        required=False,
    )

    Tag = forms.CharField(
        initial='',
        label='タグ',
        required=False,
    )

    Score = forms.CharField(
        initial='',
        label='スコア',
        required=False,  # 必須ではない
    )


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ()