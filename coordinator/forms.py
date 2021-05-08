from django import forms
from student.models import CommentAnswer

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'type something',
        'id' : 'comment',
        'name' : 'comment',
        'class' : 'form-control',
        'rows' : '3',
        'cols' : '30'
        }), label='', required=True)
    
    class Meta:
        model = CommentAnswer
        fields = ['student', 'task', 'comment']
    