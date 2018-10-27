from django import forms

from .models import Post


class UploadFileForm(forms.Form):
    '''
    부트스트랩 의존적임!
    '''
    image_file = forms.ImageField(
        # 파일입력 위젯 사용
        widget=forms.FileInput(
            # html 위젯 설정
            # form-control-file 클래스 사용
            attrs={
                'class': 'form-control-file',
            }
        )
    )
    comment = forms.CharField(
        required=False,
        # html 렌더링 위젯으로 textarea 사용
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def save(self, **kwargs):
        post = Post.objects.create(
            photo=self.cleaned_data['photo'],
            **kwargs,
        )

        # 1. comment 관련
        comment_content = self.cleaned_data.get('comment')
        if comment_content:
            post.comments.create(
                author=post.author,
                contents=comment_content,
            )

        # 2. post_list에서 각 Post의 댓글 목록을 출력
        return post


class CommentCreateForm(forms.Form):
    contents = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'forms-control',
                'rows': 2,
            }
        )
    )

    def save(self, post, **kwargs):
        contents = self.cleaned_data['contents']
        return post.comments.create(
            contents=contents,
            **kwargs,
        )