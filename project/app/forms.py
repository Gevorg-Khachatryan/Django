from django import forms
from .models import Products_photos

class NameForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)
    password = forms.CharField(label='Your password', max_length=100,widget=forms.PasswordInput)



class RegForm(forms.Form):
    name = forms.CharField(label='Your name',min_length=5, max_length=100)
    surname = forms.CharField(label='Your surname',min_length=5, max_length=100)
    email=forms.EmailField(label='Your email',min_length=5, max_length=100)
    password = forms.CharField(label='Your password', max_length=100,widget=forms.PasswordInput)
    password2 = forms.CharField(label='Conf password', max_length=100,widget=forms.PasswordInput)

class AddProductForm(forms.Form):

    name = forms.CharField(label='Product name',min_length=2, max_length=100)
    photo=forms.ImageField(label='Photo')
    #photo.widget.attrs.update({'multiple':True})
    info = forms.CharField(label='About as product',min_length=5, max_length=1000)
    options = (('Electronic', 'Electronic'),
                ('Toys', 'Toys'),
                ('Cloth','Cloth'))
    category = forms.ChoiceField(choices=options)

    price=forms.IntegerField(label='Price $')

    class Meta:
        model = Products_photos

class Message(forms.Form):
    text=forms.CharField(label='',widget=forms.Textarea)
