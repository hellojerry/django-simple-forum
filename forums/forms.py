from django import forms
from django.forms import Textarea, ModelForm
from forums.models import Thread, Post

EMPTY_ITEM_ERROR = 'SAY SOMETHING DINGUS!'
BANNED_USER_ERROR = 'SHUT IT DINGUS!'

class PostForm(forms.ModelForm):
    title = forms.CharField(required=False, widget=forms.HiddenInput())
    class Meta:
        model = Post
        fields = ['title','text']
        widgets = {
            'text': forms.Textarea(attrs={
                'cols':40,
                'placeholder': 'Start typing to make a post...',
            })}


        



'''
going to need to rig up some js to get around this issue.
'''

    



class NewThreadForm(PostForm):
    title = forms.CharField(
        max_length=100, required=True,
        error_messages={'required': EMPTY_ITEM_ERROR},
        widget=forms.TextInput(attrs={'placeholder':'Put your title here...'}))

