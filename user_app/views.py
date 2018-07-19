from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as Users
from django.contrib.auth.views import logout
from django.shortcuts import render, redirect

from user_app.email_sender import SendMail
from user_app.models import User
from .form import RegisterForm, LoginForm, ApplyForPasswordForm, ChangePasswordTrue


def index(request):
	return render(request, 'index.html')


def register(request):
	if request.user.is_authenticated:
		return redirect('/user/index/')
	else:
		pass
	if request.method == 'POST':
		register_form = RegisterForm(request.POST)
		message = '请检查填写的内容!'
		if register_form.is_valid():
			username = register_form.cleaned_data['username']
			password1 = register_form.cleaned_data['password1']
			email = register_form.cleaned_data['email']
			phone = register_form.cleaned_data['phone']
			sex = register_form.cleaned_data['sex']
			icon_path = register_form.cleaned_data['icon_png']
			if icon_path.lower() != request.session['verify_code'].lower():
				message = '验证码错误'
				return render(request, 'register.html', locals())
			else:
				del request.session['verify_code']
				user = Users.objects.create_user(
						username = username,
						password = password1
				)
				user.save()
				password1 = user.password
				new_user = User()
				new_user.name = username
				new_user.password = password1
				new_user.email = email
				new_user.phone = phone
				new_user.sex = sex
				new_user.save()
				return redirect('/user/login/')
		else:
			error_msg = register_form.errors
			return render(request, 'register.html', locals())
	else:
		register_form = RegisterForm()
		return render(request, 'register.html', locals())


def user_login(request):
	if request.user.is_authenticated:
		return redirect('/user/index/')
	else:
		if request.method == "POST":
			login_form = LoginForm(request.POST)
			message = "请检查填写的内容！"
			if login_form.is_valid():  # 确保用户名和密码都不为空
				username = login_form.cleaned_data['username']
				password = login_form.cleaned_data['password']
				icon_path = login_form.cleaned_data['icon_png']
				if icon_path.lower() != request.session['verify_code'].lower():
					message = '验证码错误'
					return render(request, 'login.html', locals())
				else:
					del request.session['verify_code']
					user = authenticate(username = username, password = password)
					if user is not None:
						login(request, user)
						return redirect('/user/index/')
					else:
						message = '用户名或密码错误'
						return render(request, 'login.html', locals())
		else:
			login_form = LoginForm()
			return render(request, 'login.html', locals())


@login_required
def user_logout(request):
	if request.user.is_authenticated:
		logout(request)
		return redirect('/user/index/')
	else:
		return redirect('/user/index/')


@login_required
def apply_for_change_password(request):
	if request.method == "POST":
		form = ApplyForPasswordForm(request.POST)
		message = "请检查填写的内容！"
		if form.is_valid():  # 密码都不为空
			icon_path = form.cleaned_data['icon_png']
			if icon_path.lower() != request.session['verify_code'].lower():
				message = '验证码错误'
				return render(request, 'login.html', locals())
			else:
				del request.session['verify_code']
				user_instance = User.objects.get(name = request.user.username)
				email_instance = user_instance.email
				target = form.cleaned_data['email']
				if email_instance != target:
					message = '不是当前用户绑定的邮箱'
					return render(request, 'apply_for_password_change.html', locals())
				else:
					# celery
					email_wait_for_deliver = SendMail(
							username = user_instance.name,
							recipient_list = [email_instance],
							url_path = "http://127.0.0.1:8000/user/change_password_true/"
					)
					result = email_wait_for_deliver.password_modify_email()
					if result == 1:
						return redirect('/user/index/')
					else:
						message = '邮件发送失败，请重新输入'
						return render(request, 'apply_for_password_change.html', locals())
	else:
		form = ApplyForPasswordForm()
		return render(request, 'apply_for_password_change.html', locals())


@login_required
def change_password_true(request):
	if request.method == 'POST':
		form = ChangePasswordTrue(request.POST)
		message = "请检查填写的内容！"
		if form.is_valid():  # 密码都不为空
			icon_path = form.cleaned_data['icon_png']
			if icon_path.lower() != request.session['verify_code'].lower():
				message = '验证码错误'
				return render(request, 'login.html', locals())
			else:
				del request.session['verify_code']
				user_instance = User.objects.get(name = request.user.username)
				user = request.user
				password1 = form.cleaned_data['password1']
				user.set_password(password1)
				user.save()
				password1 = user.password
				user_instance.password = password1
				user_instance.save()
				return redirect('/user/login/')
	else:
		form = ChangePasswordTrue()
		return render(request, 'changepassword.html', locals())