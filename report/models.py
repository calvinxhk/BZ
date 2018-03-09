from django.db import models


class UserInfo(models.Model):
    """
    用户表
    """
    nid = models.BigAutoField(primary_key=True)
    username = models.CharField(verbose_name='用户名', max_length=32, unique=True)
    password = models.CharField(verbose_name='密码', max_length=64)
    nickname = models.CharField(verbose_name='昵称', max_length=32)
    email = models.EmailField(verbose_name='邮箱', unique=True)
    avatar = models.ImageField(verbose_name='头像')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    fans = models.ManyToManyField(verbose_name='粉丝', to='UserInfo', related_name='f')


class UserFans(models.Model):
    """
    粉丝关系表
    """
    user = models.ForeignKey(verbose_name='博主', to='UserInfo', to_field='nid', related_name='users')
    followers = models.ForeignKey(verbose_name='粉丝', to='UserInfo', to_field='nid', related_name='followers')

    class Meta:
        unique_together = [
            ('user', 'followers'),
        ]


class Blog(models.Model):
    """
     博客表
    """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='博客标题', max_length=64)
    site = models.CharField(verbose_name='博客前缀', max_length=32, unique=True)
    theme = models.CharField(verbose_name='博客主题', max_length=32)
    user = models.OneToOneField(to='UserInfo', to_field='nid')


class Category(models.Model):
    """
    个人文章分类表
    """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')


class Tag(models.Model):
    """
    标签表
    """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名字', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')


class Article(models.Model):
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='文章标题', max_length=128)
    summary = models.CharField(verbose_name='文章简介', max_length=255)
    read_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    create_time = models.DateTimeField(verbose_name='发表时间', auto_now_add=True)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')
    category = models.ForeignKey(verbose_name='文章类型', to="Category", to_field="nid", null=True)
    type_choices = [(1, 'Python'), (2, 'Linux'), (3, 'MySQL'), (4, 'GOLang')]
    article_type_id = models.IntegerField(choices=type_choices, default=None)
    tags = models.ManyToManyField(to='Tag', through='Article2Tag')


class ArticleDetail(models.Model):
    """
    文章内容表
    """
    content = models.TextField(verbose_name='文章内容')
    article = models.OneToOneField(verbose_name='文章信息', to='Article', to_field='nid')


class Article2Tag(models.Model):
    article = models.ForeignKey(verbose_name='文章', to='Article', to_field='nid')
    tag = models.ForeignKey(verbose_name='标签', to='Tag', to_field='nid')

    class Meta:
        unique_together = [('article','tag')]