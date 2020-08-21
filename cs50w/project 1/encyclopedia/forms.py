from django import forms

class Create(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    content = forms.CharField(label='Content', widget=forms.Textarea(attrs={"style": "height: 50vh"}))

class EditPage(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    content = forms.CharField(label='Content', widget=forms.Textarea(attrs={"style": "height: 50vh"}))
