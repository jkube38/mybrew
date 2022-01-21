# from django.shortcuts import render
from django.http import HttpResponse
from itertools import chain
from my_brew_notifications.models import UserPostNotification
from my_brew_notifications.models import UserCommentNotification


# generates a list of notifications for the current user
def header_notifications_view(request):
    notifications_post = UserPostNotification.objects.filter(
        user_mentioned__username=request.user.username)

    notifications_comment = UserCommentNotification.objects.filter(
        user_mentioned__username=request.user.username
    )

    notifications = list(chain(notifications_post, notifications_comment))

    ordered_notifications = sorted(notifications, key=lambda x: x.created_at)

    notification_list = []
    new_notifications = False

    for notification in ordered_notifications:
        notification_list.append(notification)
        if notification.viewed is False:
            new_notifications = True
    notification_list.reverse()

    return (notification_list, new_notifications)


# when a notification is viewed the viewed value is turned to true
# using jquery and displays accordingly
def notification_viewed_view(request, notification_id):

    if notification_id[-1] == 'p':
        notification = UserPostNotification.objects.get(
            pk=notification_id[:-1])
        notification.viewed = True
        notification.save()
    else:
        notification = UserCommentNotification.objects.get(
            pk=notification_id[:-1])
        notification.viewed = True
        notification.save()

    userPostNotifications = UserPostNotification.objects.filter(
        user_mentioned__username=request.user.username, viewed=False)

    userCommentNotifications = UserCommentNotification.objects.filter(
        user_mentioned__username=request.user.username, viewed=False)

    if userPostNotifications or userCommentNotifications:
        new_notifications = True
    else:
        new_notifications = False
    return HttpResponse(new_notifications)


# allows the user to delete a notification when they are done with it
def notification_delete_view(request, notification_id):
    if notification_id[-1] == 'p':
        notification = UserPostNotification.objects.get(
            pk=notification_id[:-1])
        notification.delete()
    else:
        notification = UserCommentNotification.objects.get(
            pk=notification_id[:-1])
        notification.delete()
    return HttpResponse()
