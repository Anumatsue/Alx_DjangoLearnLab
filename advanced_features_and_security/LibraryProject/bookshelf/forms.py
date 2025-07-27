from django import forms

"""class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)"""


class ExampleForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(widget=forms.Textarea, label='Your Message')