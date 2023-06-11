
# import the standard Django Forms
# from built-in library
from django import forms
from .models import USER_TYPES
from django.utils.safestring import mark_safe
# creating a form 
class ProfileForm(forms.Form):
    
    username = forms.CharField(required=True, max_length = 200)
    register_as = forms.CharField(required=True,max_length=200,label=mark_safe('<br/>User Type'), widget=forms.Select(choices=USER_TYPES,attrs={ 'style': 'margin-right:0px; width:130;margin-top:10px'}))
    profile_picture = forms.ImageField(required=False,label=mark_safe('<br />Profile Picture')
    , widget = forms.FileInput(attrs = { 'style' : "height: 30px ; width : 90px ; margin-right:-8px;margin-top:10px" } ))
    