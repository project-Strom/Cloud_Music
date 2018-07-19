from datetime import datetime

from django.db import models


class Singer(models.Model):
	"""
	歌手跟歌曲是一对多关系
	歌手跟专辑是一对多关系
	name 歌手名称
	classification歌手分类(枚举)
	introduction歌手简介
	image歌手头像
	"""
	image = models.ImageField(null = True)
	name = models.CharField(max_length = 100, null = False, unique = False)
	introduction = models.CharField(max_length = 200, null = False)

	def __str__(self):
		return self.name


class Album(models.Model):
	"""
	专辑和歌手是多对一关系
	name 专辑名称
	release_time 发布时间
	poster 专辑海报
	introduction 简介
	"""
	poster = models.ImageField(null = True)
	name = models.CharField(max_length = 100, null = False, unique = False)
	introduction = models.IntegerField(null = False)
	release_time = models.DateField(null = True)
	singer = models.ForeignKey(
			Singer,
			null = True,
			on_delete = models.SET_NULL,
			related_name = 'album_belong_to_singer',
			related_query_name = 'album_query_by_singer'
	)

	def __str__(self):
		return self.name


class Music(models.Model):
	"""
	歌曲和专辑是多对一的关系
	name 歌曲名称
	release_time 歌曲发布时间
	url_address 歌曲url地址
	playing_counts 播放次数
	delete_status 是否删除
	free_status 是否免费
	price 价格
	introduction 简介
	"""
	name = models.CharField(max_length = 40, null = False, unique = False)
	release_time = models.DateField(null = True)
	url_address = models.URLField(max_length = 200, null = True)
	playing_counts = models.IntegerField(null = False, default = 0)
	delete_status = models.NullBooleanField(null = True)
	free_status = models.NullBooleanField(null = True)
	price = models.FloatField(max_length = 3)
	introduction = models.CharField(max_length = 200, null = True)
	album = models.ForeignKey(
			Album,
			null = True,
			on_delete = models.SET_NULL,
			related_name = 'musics_belong_to_album',
			related_query_name = 'album_query_by_music'
	)
	music_bind_singer = models.ForeignKey(
			Singer,
			null = True,
			on_delete = models.SET_NULL,
			related_name = 'musics_belong_to_singer',
			related_query_name = 'singer_query_by_music'
	)

	def __str__(self):
		return self.name


class User(models.Model):
	"""
	name 用户名称（char field）
	sex 用户性别（bool filed）
	age 用户年龄（int filed）
	password 密码(char filed)
	email (email field)
	phone(char filed 自己验证)
	introduction（text field）
	icon(image field)
	last_log_in_time(date time field)
	follower()
	"""
	name = models.CharField(max_length = 100, null = False, unique = True)
	# 最好采用枚举
	sex = models.NullBooleanField()
	age = models.IntegerField(null = True)
	password = models.CharField(max_length = 200)
	email = models.EmailField(null = False)
	phone = models.CharField(max_length = 20, null = True)
	introduction = models.TextField(null = True)
	# 设置upload_to
	icon = models.ImageField(null = True)
	last_log_in_time = models.DateTimeField(default = datetime.utcnow())
	token = models.CharField(max_length = 200, null = True)
	"""
	用户自己的收藏
	跟歌曲是多对多关系
	"""
	music_collection = models.ManyToManyField(
			Music,
			through = 'FavoriteList',
			through_fields = ('user', 'music')
	)

	def __str__(self):
		return self.name


class FavoriteList(models.Model):
	user = models.ForeignKey(
			User,
			null = True,
			on_delete = models.SET_NULL,
			related_name = 'music_list_collected_by_user',
			related_query_name = 'user_query_by_collected_music_list'
	)
	music = models.ForeignKey(
			Music,
			null = True,
			on_delete = models.SET_NULL,
			related_name = 'music_collected_in_music_list',
			related_query_name = 'music_list_query_by_music_collected'
	)
	date = models.DateTimeField(auto_now = True)


class Comment(models.Model):
	"""
	评论和歌曲是一对多关系
	评论和歌单是一对多关系
	title 评论标题
	text 评论
	parent_comment 父评论
	"""
	title = models.CharField(max_length = 100, null = True)
	text = models.TextField(null = False)
	parent_comment = models.ForeignKey(
			'self',
			null = True,
			on_delete = models.CASCADE
	)
	user = models.ForeignKey(
			User,
			null = True,
			on_delete = models.SET_NULL,
			related_name = 'comments_by_user',
			related_query_name = 'user_query_by_comments'
	)
	music = models.ForeignKey(
			Music,
			null = True,
			on_delete = models.SET_NULL,
			related_name = 'comments_in_music',
			related_query_name = 'music_query_by_comments'
	)

	def result(self):
		return isinstance(self.parent_comment, type(None))

	def __str__(self):
		results = 'None' if self.result() else self.parent_comment.text
		return '''  <Title>:{} <Content>:{} <parent_Title>:{}'''.format(self.title, self.text, results)


class MusicSheet(models.Model):
	"""
	歌单和用户是多对一关系
	歌单和歌曲是多对多关系
	name 歌单名称
	release_time 发布时间
	poster 歌单海报
	introduction 简介
	view_counts 被试听次数
	collected_counts 被收藏次数
	"""
	poster = models.ImageField(height_field = 100, width_field = 100)
	name = models.CharField(max_length = 100, null = False, unique = False)
	introduction = models.IntegerField(null = False)
	release_time = models.DateField(null = True)
	viewed_times = models.IntegerField(default = 0)
	collected_times = models.IntegerField(default = 0)
	user = models.ForeignKey(
			User,
			null = True,
			on_delete = models.SET_NULL,
			related_name = 'music_sheet_beyond_to_user',
			related_query_name = 'user_query_by_music_sheet',
	)
	music = models.ManyToManyField(
			Music,
			through = 'MusicToMusicSheet',
			# through_fields = ('music', 'music_sheet'),
	)

	user_collection = models.ManyToManyField(
			User,
			through = 'MusicSheetCollection'
	)


class MusicToMusicSheet(models.Model):
	music = models.ForeignKey(
			Music,
			null = True,
			on_delete = models.SET_NULL,
			related_name = 'music_collected_in_music_sheet',
			related_query_name = 'music_sheet_query_by_music'
	)
	music_sheet = models.ForeignKey(
			MusicSheet,
			null = True,
			on_delete = models.SET_NULL,
	)
	date = models.DateTimeField(auto_now = True)


class MusicSheetCollection(models.Model):
	user = models.ForeignKey(
			User,
			null = True,
			on_delete = models.SET_NULL,
			related_name = 'music_sheet_collected_by_user',
			related_query_name = 'user_query_by_music_sheet'
	)
	music_sheet = models.ForeignKey(
			MusicSheet,
			null = True,
			on_delete = models.SET_NULL,
	)