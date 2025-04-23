from django import forms

class WishUpdate(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    notes = forms.CharField(max_length=1000, widget=forms.Textarea, required=False)
    link = forms.URLField(required=False)
    status = forms.BooleanField(required=False, initial=False)
    

    

class DeleteForm(forms.Form):
    deletion = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput)


class ListUpdate(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    description = forms.CharField(max_length=1000, widget=forms.Textarea, required=False)