from django import forms

class File_input_form(forms.Form):
    file=forms.FileField(label='Choose')
