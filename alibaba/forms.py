from django import forms
from alibaba.models import user
class UserForm(forms.ModelForm):
    class Meta:
        model=user
        fields='__all__'