from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Nombre de usuario"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Ingrese su password", "class":"form-control"}))
