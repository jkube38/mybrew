from my_brew_app.models import MyBrewUser
from my_brew_posts.models import UserPost, PostComment
import itertools


def sort_posts(request, username):

    if request.user.username == username:
        '''USERS HOME PAGE/ Gathers a list of posts created by people
            and breweries the current user is following and sorts them
            by the newest first and returns a list of tuples with the
            post and a list of the people who have liked it'''
        user = MyBrewUser.objects.get(username=request.user.username)
        following = [follow for follow in user.followed_user.all()]

        relevent_post_list = []

        for follow in following:
            follow_posts = UserPost.objects.filter(created_by=follow)
            relevent_post_list.append(follow_posts)

        last_hundred = list(itertools.chain.from_iterable(relevent_post_list))
        relevent_posts = sorted(last_hundred, key=lambda x: x.created_at)
        relevent_posts.reverse()
        last_hundred = relevent_posts[:100]

        final_post_list = []
        for post in last_hundred:

            post_comments = []
            comments = PostComment.objects.filter(target_post__id=post.pk)
            if comments:
                for comment in comments:
                    post_comments.append(comment)
            likes_usernames = []
            likes = post.liked_by.all()
            for like in likes:
                likes_usernames.append(like.username)
            final_post_list.append((post, likes_usernames, post_comments))
        return final_post_list
    else:
        '''When visiting another users profile this will produce a list of
            users posts and return them in a tuple with all the
            corresponding likes'''

        followed_user_posts = UserPost.objects.filter(
            created_by__username=username)

        last_hundred = []

        for post in followed_user_posts:

            post_comments = []
            comments = PostComment.objects.filter(target_post__id=post.pk)
            if comments:
                for comment in comments:
                    post_comments.append(comment)
            likes_usernames = []
            likes = post.liked_by.all()
            for like in likes:
                likes_usernames.append(like.username)
            last_hundred.append((post, likes_usernames, post_comments))
        last_hundred.reverse()
        final_post_list = last_hundred[:100]
        return final_post_list


def current_user_posts(request):
    current_user = request.user.username
    cu_posts = UserPost.objects.filter(created_by__username=current_user)
    cu_post_list = []

    for post in cu_posts:

        like_usernames = []
        likes = post.liked_by.all()
        for like in likes:
            like_usernames.append(like.username)

        post_comments = []
        comments = PostComment.objects.filter(target_post__id=post.pk)
        if comments:
            for comment in comments:
                post_comments.append(comment)
        cu_post_list.append((post, like_usernames, post_comments))
    cu_post_list.reverse()
    return cu_post_list


def all_current_posts():
    current_posts = UserPost.objects.order_by('created_at')[:100]

    current_post_list = []
    for post in current_posts:

        like_usernames = []
        likes = post.liked_by.all()
        for like in likes:
            like_usernames.append(like.username)

        post_comments = []
        comments = PostComment.objects.filter(target_post__id=post.pk)
        if comments:
            for comment in comments:
                post_comments.append(comment)
        current_post_list.append((post, like_usernames, post_comments))
    current_post_list.reverse()
    return current_post_list
