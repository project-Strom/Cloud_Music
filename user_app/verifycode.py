import hashlib
from io import BytesIO

from django.http import HttpResponse


def verify_code(request):
	# 引入绘图模块
	from PIL import Image, ImageDraw, ImageFont
	import random

	# 定义变量，用于画面的背景色，宽，高
	background_color = (random.randrange(20, 100), random.randrange(20, 100), 0)
	width = 100
	height = 25

	# 创建画面对象
	im = Image.new('RGB', (width, height), background_color)  # 画布

	# 创建画笔对象
	draw = ImageDraw.Draw(im)  # 此画笔用于画面对象书写

	# 调用画笔的point()函数给画布对象绘制噪点
	for i in range(0, 100):
		xy = (random.randrange(0, width), random.randrange(0, height))  # 变量，只不过就被叫做xy，叫做a, b, 任何东西都可以
		fill = (random.randrange(0, 255), 255, random.randrange(0, 255))  # (R, G, B) 随机生成三原色
		draw.point(xy, fill = fill)  # 把点画上去

	str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
	rand_str = ''
	for i in range(0, 4):
		rand_str += str1[random.randrange(0, len(str1))]
	# 生成4位验证码

	# 构造字体对象
	font = ImageFont.truetype(font = 'static/font/hktt.ttf', size = 23)

	# 构造字体颜色
	font_color = (255, random.randrange(0, 255), random.randrange(0, 255))

	# 绘制四个字体
	draw.text((5, 2), rand_str[0], font = font, fill = font_color)
	draw.text((25, 2), rand_str[1], font = font, fill = font_color)
	draw.text((50, 2), rand_str[2], font = font, fill = font_color)
	draw.text((75, 2), rand_str[3], font = font, fill = font_color)

	# 存入session，用于做进一步验证
	request.session['verify_code'] = rand_str

	buffer = BytesIO()  # 缓存
	im.save(buffer, 'png')  # 指定图片的格式为png

	# 释放画笔
	del draw
	del im
	return HttpResponse(buffer.getvalue(), 'image/png')


def hash_code(s, salt = 'mysite'):  # 加点盐
	h = hashlib.sha256()
	s += salt
	h.update(s.encode())  # update方法只接收bytes类型
	return h.hexdigest()
