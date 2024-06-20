from django import forms

from .models import User, Post, Comment


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author']
        widgets = {
            'pub_date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
