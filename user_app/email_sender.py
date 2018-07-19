from django.core.mail import EmailMultiAlternatives

from Cloud_Music.settings import EMAIL_HOST_USER


class SendMail(object):
	def __init__(self, username, recipient_list, url_path):
		self.url_path = url_path
		self.username = username
		self.recipient_list = recipient_list

	def password_modify_email(self):
		subject = '用户密码修改',
		from_email = EMAIL_HOST_USER
		text_content = '用户{},你好，如果要修改密码，请点击下面的链接完成密码修改'.format(self.username)
		html_content = '<strong><a href="{}">点击修改密码</a></strong>'.format(self.url_path)
		message = EmailMultiAlternatives(
				subject = subject,
				body = text_content,
				from_email = from_email,
				to = self.recipient_list
		)
		message.attach_alternative(content = html_content, mimetype = "text/html")
		result = message.send()
		return result
