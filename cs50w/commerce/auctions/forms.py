from django import forms
from .models import *

class NewListing(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('title', 'description', 'price', 'image', 'category',)

class PlaceBid(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('amount',)

class NewComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
        widgets={
            'comment': forms.TextInput(
                attrs={'style': 'width:100%;height:50px'}
                )
        }