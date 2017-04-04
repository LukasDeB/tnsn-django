from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Posts
from django.forms import ModelForm, Textarea

class AccountForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = {
            'username',
            'email',
            'password1',
            'password2'
        }

    def save(self, commit=True):
        user = super(AccountForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class PostForm(ModelForm):
    class Meta:
        model = Posts
        fields = ['content']
        exclude = ['author']

    
