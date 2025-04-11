from django import forms

from .models import User, Order


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
