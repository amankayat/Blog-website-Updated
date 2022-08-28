from django import forms
from App_Blog.models import Blog,comment

class commmentForm(forms.ModelForm):
    class Meta:
        model = comment
        fields = ('comment',)