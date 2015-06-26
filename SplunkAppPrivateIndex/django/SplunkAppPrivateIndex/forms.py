
from django import forms
 
class SecuredIndexForm(forms.Form):
    index_name = forms.CharField(max_length=255)
    role_name = forms.CharField(max_length=255)
    group_name = forms.CharField(max_length=255)

