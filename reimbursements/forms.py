from django import forms

from .models import Ad


class CreateAdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ["ad_type", "spend"]


class RemoveAdForm(forms.Form):
    pk = forms.IntegerField()
