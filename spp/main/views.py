from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *

def Logout(request):
	logout(request)
	return redirect('Loggin/')

def login_page(request):
	message=None
	if 'Usuario' in request.session:
		return redirect("/SPP/")
	else:
		if request.method=="POST":
			form = LoginForm(request.POST)
			if form.is_valid():
				username = request.POST['username']
				password = request.POST['password']
				user = authenticate(username=username, password=password)
				if user is not None:
					if user.is_active:
						login(request, user)
						request.session['Usuario'] = username
						return redirect("/SPP/")
					else:
						message ="Usuario no esta activo contacta al admin"
				else:
					message = "Nombre de usuario y/o Contrasena no valido"
		else:
			form = LoginForm()
		return render(request, 'login.html', {'message': message, 'form': form})