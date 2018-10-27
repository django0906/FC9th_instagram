# from django.contrib.auth.models import AbstractUser
import datetime
import re

from django.db import models
from django.conf import settings

# https://github.com/matthewwithanm/django-imagekit


class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(
        # Django가 기본적으로 제공하는 User 클래스
        # 'appname.modelname'
        # 'members.User',
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='작성자',
    )

    photo = models.ImageField(
        '사진',
        upload_to='post',
    )

    class Meta:
        verbose_name = '포스트'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ('-pk',)


class Comment(models.Model):
    TAG_PATTERN = re.compile(r'#(?P<tag>\w+)')

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='포스트',
        related_name='comments',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # 'members.User',
        on_delete=models.CASCADE,
        verbose_name='작성자',
    )
    contents = models.TextField()
    # 해시태그: 여러개
    hashtags = models.ManyToManyField(
        'Hashtags',
        blank=True,
        verbose_name='해시태그 목록',
    )
    # Comment의 save()가 호출 될 때,
    # content의 값을 사용해서 이 필드를 자동으로 채운 후 저장하기
    _html = models.TextField('태그가 HTML화된 댓글 내용', blank=True)

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = f'{verbose_name} 목록'
    # 멘션을 달면 나와 남이 바로연계됨.
    # mentions = models.ManyToManyField(
    #     'User',
    # )

    # 댓글 저장 후, content에 포함된 Hashtags 목록을
    # 댓글의 tags 속성에 set한다.
    # 원래 views에 있던걸 save 메소드 overriding으로 해치움.
    def save(self, *args, **kwargs):
        def save_html():
            # 저장하기 전에 _html필드를 채워야 함 (content값을 사용해서)
            self._html = re.sub(
                self.TAG_PATTERN,
                r'<a href="/explore/tags/\g<tag>/">#\g<tag></a>',
                self.contents,
            )

        def save_hashtags():
            # DB에 Comment저장이 완료된 후,
            #  자신의 'content'값에서 해시태그 목록을 가져와서
            #  자신의 'tags'속성 (MTM필드)에 할당
            hashtags = [Hashtags.objects.get_or_create(tag_name=tag_name)[0]
                        for tag_name in re.findall(self.TAG_PATTERN, self.contents)]
            self.hashtags.set(hashtags)

        save_html()
        super().save(*args, **kwargs)
        save_hashtags()

    @property
    def html(self):
        # 자신의 content속성값에서
        # "#태그명"에 해당하는 문자열을
        #  아래와 같이 변경
        #   <a href="/explore/tags/{태그명}>/">#{태그명}</a>
        # re.sub를 사용
        return self._html


class Hashtags(models.Model):
    tag_name = models.CharField(
        '태그명',
        max_length=64,
        unique=True,
    )

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name = '해시태그'
        verbose_name_plural = f'{verbose_name} 목록'
