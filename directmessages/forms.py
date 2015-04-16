from .models import DirectMessage
from django import forms

class ComposeForm(forms.ModelForm):
    class Meta:
        model = DirectMessage
        fields = ['subject', 'text']
        widgets = {
            'text': forms.Textarea(attrs={
                'cols':60,
                'rows':10,
                'placeholder': 'Start typing to compose a message...'}),
            'subject':forms.Textarea(attrs={
                'cols':116,
                'rows': 1,
                'placeholder': 'Put the subject line here...'
            })
        }
        
class MessageReplyForm(ComposeForm):
    subject = forms.CharField(required=False, widget=forms.HiddenInput())
    fields = ['text']
    widgets = {
        'text': forms.Textarea(attrs={
            'cols':60,
            'placeholder': 'Start typing to compose a reply...'
        })
    }
    
