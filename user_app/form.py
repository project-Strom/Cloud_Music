import re

from django import forms
from django.core.exceptions import ValidationError

from user_app.models import User


def style_email_validator(values):
	"""
	自定义邮箱匹配
	:param values:
	:return:
	"""
	email_re = re.compile(r'^.*?@(qq|163|gmail|foxmail)\.com$')
	if email_re.match(values):
		return True
	else:
		raise ValidationError('当前邮箱不支持')


def style_name_validator(values):
	"""
	自定义用户名称匹配
	:param values:
	:return:
	"""
	name_re = re.compile(r'^[a-zA-Z0-9_-]{4,16}$')
	if name_re.match(values):
		return True
	else:
		raise ValidationError('4到16位（字母，数字，下划线，减号')


def style_password_intensity_validator(values):
	"""
	密码强度验证
	:return:
	"""
	password_re = re.compile(r'^.*(?=.{6,})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*? ]).*$')
	if password_re.match(values):
		return True
	else:
		return True


def style_phone_validator(values):
	"""
	电话号码验证
	:param values:
	:return:
	"""
	phone_re = re.compile(r'^((13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\d{8}$')
	if phone_re.match(values):
		return True
	else:
		raise ValidationError('电话号码格式不正确')


class RegisterForm(forms.Form):
	"""
	给form类自定义验证规则，如果想要重用验证机制，可以单独创建新的字段类，重新写它的验证方法。
	一般的可以直接在form类加入clean_字段名的方法，Django会自动查找以clean_开头的函数名，并会在
	验证该字段的时候，运行这个函数。
	"""
	gender = (
		(0, "男"),
		(1, "女"),
	)

	username = forms.CharField(
			label = '用户名称',
			max_length = 50,
			required = True,
			error_messages = {
				'required': '用户名不能为空'
			},
			widget = forms.TextInput(attrs = {'class': 'form-control'})
	)

	password1 = forms.CharField(
			label = '用户密码',
			min_length = 6,
			max_length = 100,
			required = True,
			error_messages = {
				'required': '密码不能为空'
			},
			widget = forms.TextInput(attrs = {'class': 'form-control', 'type': 'password'})
	)

	password2 = forms.CharField(
			label = '用户确认密码',
			min_length = 6,
			max_length = 100,
			required = True,
			error_messages = {
				'required': '密码不能为空',
			},
			widget = forms.TextInput(attrs = {'class': 'form-control', 'type': 'password'})
	)

	email = forms.EmailField(
			label = '用户邮箱',
			required = True,
			error_messages = {
				'required': '邮箱不能为空',
			},
			widget = forms.TextInput(attrs = {'class': 'form-control'})
	)

	phone = forms.CharField(
			label = '用户电话号码',
			max_length = 11,
			min_length = 11,
			required = True,
			error_messages = {
				"required": '电话号码不能为空',
			},
			widget = forms.TextInput(attrs = {'class': 'form-control'})

	)
	sex = forms.ChoiceField(label = '性别', choices = gender)
	icon_png = forms.CharField(
			label = '验证码',
			max_length = 10,
			widget = forms.TextInput(attrs = {'class': 'form-control'})
	)

	def clean_username(self):
		name = self.cleaned_data['username']
		if style_name_validator(name):
			if User.objects.filter(name = name).count():
				raise ValidationError('用户名已被注册')
			else:
				return name

	def clean_email(self):
		email = self.cleaned_data['email']
		if style_email_validator(email):
			if User.objects.filter(email = email).count():
				raise ValidationError('邮箱已被注册')
			else:
				return email

	def clean_phone(self):
		phone = self.cleaned_data['phone']
		if style_phone_validator(phone):
			if User.objects.filter(phone = phone):
				raise ValidationError('电话号码已被注册')
			else:
				return phone

	def clean(self):
		password11 = self.cleaned_data['password2']
		password22 = self.cleaned_data['password1']

		if password11 != password22:
			raise forms.ValidationError('两次输入密码不匹配')
		else:
			style_password_intensity_validator(password11)


class LoginForm(forms.Form):
	username = forms.CharField(
			label = 'user_name',
			max_length = 50,
			required = True,
			error_messages = {
				'required': '用户名不能为空'
			},
			widget = forms.TextInput(attrs = {'class': 'form-control'})

	)
	password = forms.CharField(
			label = 'password',
			min_length = 6,
			max_length = 100,
			required = True,
			error_messages = {
				'required': '密码不能为空'
			},
			widget = forms.TextInput(attrs = {'class': 'form-control', 'type': 'password'})
	)

	icon_png = forms.CharField(
			label = '验证码',
			max_length = 10,
			widget = forms.TextInput(attrs = {'class': 'form-control'})
	)


class ApplyForPasswordForm(forms.Form):
	email = forms.EmailField(
			label = '用户邮箱',
			required = True,
			error_messages = {
				'required': '邮箱不能为空',
			},
			widget = forms.TextInput(attrs = {'class': 'form-control'})
	)
	icon_png = forms.CharField(
			label = '验证码',
			max_length = 10,
			widget = forms.TextInput(attrs = {'class': 'form-control'})
	)


class ChangePasswordTrue(forms.Form):
	password1 = forms.CharField(
			label = '用户密码',
			min_length = 6,
			max_length = 100,
			required = True,
			error_messages = {
				'required': '密码不能为空'
			},
			widget = forms.TextInput(attrs = {'class': 'form-control', 'type': 'password'})
	)

	password2 = forms.CharField(
			label = '用户确认密码',
			min_length = 6,
			max_length = 100,
			required = True,
			error_messages = {
				'required': '密码不能为空',
			},
			widget = forms.TextInput(attrs = {'class': 'form-control', 'type': 'password'})
	)
	icon_png = forms.CharField(
			label = '验证码',
			max_length = 10,
			widget = forms.TextInput(attrs = {'class': 'form-control'})
	)

	def clean(self):
		password11 = self.cleaned_data['password2']
		password22 = self.cleaned_data['password1']
		if password11 != password22:
			raise forms.ValidationError('两次输入密码不匹配')
		else:
			style_password_intensity_validator(password11)