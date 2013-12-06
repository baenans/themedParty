# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from www.models import Profiles, Characters
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

@login_required(login_url='/login/')
def home(request):
	profile = Profiles.objects.get(user=request.user)
	if profile.character:
		return redirect('profile')
	else:
		return redirect('select')

@login_required(login_url='/login/')
def profile(request):
	if request.method == 'POST':
		pf = Profiles.objects.get(user=request.user)
		oldC = Characters.objects.get(id=pf.character.id)
		oldC.taken = False
		oldC.save()
		pf.character = None
		pf.save()
		return redirect('select')
	else:
		profile = Profiles.objects.get(user=request.user)
		character = Characters.objects.get(id=profile.character.id)
		return render(request, 'index.htm', {	'profile':profile,
												'char':character})
@login_required(login_url='/login/')
def select(request):
	if request.method == 'POST':
		pf = Profiles.objects.get(user=request.user)
		newC = Characters.objects.get(id=request.POST['schar'])
		newC.taken = True
		newC.save()
		pf.character = Characters(id=request.POST['schar'])
		pf.save()
		return redirect('profile')
	else:
		profile = Profiles.objects.get(user=request.user)
		try:
			chars = Characters.objects.filter(taken=False, sex=profile.sex)
		except Characters.DoesNotExist:
			chars = None
		return render(request, 'chars.htm', {'chars':chars})

def loginView(request):
	if request.user.is_authenticated():
		return redirect('home')
	else:
		if request.method=='POST':
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('home')
				else:
					error = 'Su cuenta ha sido deshabilitada.'
					context = {'error': error}
					return render(request, 'login.htm', context)
			else:
				error = 'Su nombre de usuario o contraseña son incorrectos'
				context = {'error': error}
				return render(request, 'login.htm', context)
		else:
			return render(request, 'login.htm', {})

def logoutView(request):
	logout(request)
	return redirect('loginView')