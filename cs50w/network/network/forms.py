from django import forms
from .models import *

class NewPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text',)
