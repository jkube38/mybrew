from django.http.response import HttpResponse
from my_brew_posts.forms import UserPostForm, PostCommentForm
from my_brew_app.models import MyBrewUser
from my_brew_posts.models import UserPost, PostComment
from my_brew_notifications.models import UserPostNotification
import re


# Create your views here.
def user_post_view(request):
    user = MyBrewUser.objects.get(username=request.user.username)
    if request.is_ajax():
        post_form = UserPostForm(request.POST, request.FILES)
        if post_form.is_valid():
            data = post_form.cleaned_data
            new_post = UserPost.objects.create(
                post=data['post'],
                created_by=user,
                post_pic=data['post_pic']
            )

            # Looks for a mention and creates a notification
            mention_search = data['post']
            mention_re = re.compile(r'(@[^\s,.:\'"!#$%^&*()]+)')
            post_search = mention_re.findall(mention_search)
            if post_search:
                for mention in post_search:
                    try:
                        at_user = mention[1:]
                        if at_user != request.user.username:
                            user_mentioned = MyBrewUser.objects.get(
                                username=at_user)
                            posted_by = MyBrewUser.objects.get(
                                username=request.user.username)
                            target_post = UserPost.objects.get(id=new_post.pk)
                            UserPostNotification.objects.create(
                                posted_by=posted_by,
                                user_mentioned=user_mentioned,
                                target_post=target_post
                            )
                    except (MyBrewUser.DoesNotExist):
                        remove_at = mention_search.replace(
                            mention, mention[1:])
                        new_post.post = remove_at
                        new_post.save()
    return HttpResponse()


def post_like_view(request, username, post_id):
    '''Allows the users to like a post by clicking the like link
        updates the number of likes and the user who liked it in
        the post model'''
    post_like = UserPost.objects.get(id=post_id)
    if post_like.likes is None:
        post_like.likes = 1
        post_like.liked_by.add(request.user)
    else:
        post_like.likes += 1
        post_like.liked_by.add(request.user)
    post_like.save()
    return HttpResponse()


def post_comment_data_view(request, post_commenter, post_id, post_creator):

    comment_data = {
        'comment_author': post_commenter,
        'post_target': post_id,
        'post_author': post_creator
    }

    request.session['comment_data'] = comment_data
    return HttpResponse()


def post_comment_view(request):

    comment_data = request.session.get('comment_data')
    comment_author = MyBrewUser.objects.get(
        username=comment_data['comment_author'])
    post_target = UserPost.objects.get(id=comment_data['post_target'])
    post_author = MyBrewUser.objects.get(username=comment_data['post_author'])

    if request.is_ajax():
        form = PostCommentForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            if data['comment_pic']:
                PostComment.objects.create(
                    commenter=comment_author,
                    target_post=post_target,
                    comment=data['comment'],
                    post_creator=post_author,
                    comment_pic=data['comment_pic']
                )
            else:
                PostComment.objects.create(
                    commenter=comment_author,
                    target_post=post_target,
                    comment=data['comment'],
                    post_creator=post_author
                )
        post_id = post_target.id
    return HttpResponse(post_id)
