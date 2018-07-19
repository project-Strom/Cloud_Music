from django.db import models


# Create your models here.
class Singer(models.Model):
	"""
	歌手和歌曲一对多，歌手和专辑一对多
	"""
	name = models.CharField(max_length = 100, null = False, unique = False)
	image = models.ImageField(null = True)
	introduction = models.TextField(null = False)

	def __str__(self):
		return self.name


class Album(models.Model):
	"""
	专辑和歌手多对一，专辑和歌曲一对多
	"""
	poster = models.ImageField(null = True)  # 海报图片
	name = models.CharField(max_length = 100, null = False, unique = False)
	introduction = models.TextField(null = False)
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


class MusicSheet(models.Model):
	name = models.CharField(max_length = 200)
	create_time = models.DateTimeField(null = True)
	collect_count = models.IntegerField()
	icon_path = models.ImageField(null = True)


class Music(models.Model):
	"""

	"""
	name = models.CharField(max_length = 100, null = False, unique = False)
	release_time = models.DateField(null = True)
	url_address = models.URLField(max_length = 200, null = False)
	play_counts = models.IntegerField(null = False, default = 0)
	delete_status = models.NullBooleanField()
	free_status = models.NullBooleanField()
	price = models.FloatField(max_length = 3)
	introduction = models.CharField(max_length = 200, null = True)

	music_sheet = models.ManyToManyField(MusicSheet)

	album = models.ForeignKey(
			Album,
			null = True,
			on_delete = models.SET_NULL,
			related_name = 'music_belong_to_album',
			related_query_name = 'album_query_by_music'
	)

	music_bind_singer = models.ForeignKey(
			Singer,
			null = True,
			on_delete = models.SET_NULL,
			related_name = 'music_belong_to_singer',
			related_query_name = 'singer_query_by_music'
	)

	def __str__(self):
		return self.name


class User(models.Model):
	"""

	"""
	name = models.CharField(max_length = 100, null = False, unique = True)
	sex = models.CharField(max_length = 5, default = 'male')
	age = models.IntegerField(null = True)
	password = models.CharField(max_length = 200)
	email = models.EmailField(null = False)
	phone = models.CharField(max_length = 20, null = True)
	introduction = models.TextField(null = True)
	icon = models.ImageField()
	last_login_time = models.DateTimeField(null = True)
	token = models.CharField(max_length = 200, null = True)

	def __str__(self):
		return self.name

	# User与Music多对多
	music = models.ManyToManyField(Music)

	music_sheet = models.ManyToManyField(MusicSheet)


class Comment(models.Model):
	"""
	评论和歌曲多对一，评论和歌单多对一
	"""
	title = models.CharField(max_length = 100, null = True)
	text = models.TextField(null = False)

	music = models.ForeignKey(
			Music,
			null = True,
			on_delete = models.SET_NULL,
			related_name = 'comment',
	)

	music_sheet = models.ForeignKey(
			MusicSheet,
			null = True,
			on_delete = models.SET_NULL,
			related_name = 'comment'
	)

	def __str__(self):
		return self.text

# class MusicKinds(models.Model):  分类，暂时搞不了