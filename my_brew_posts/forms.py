from django import forms


class UserPostForm(forms.Form):
    post = forms.CharField(
        label='',
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': 'review, comment, share, @username to mention'
        })
    )
    post_pic = forms.FileField(label='', required=False)


class PostCommentForm(forms.Form):
    comment = forms.CharField(
        label='',
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': 'comment'
        })
    )
    comment_pic = forms.FileField(label='', required=False)
