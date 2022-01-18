# from django.shortcuts import render
from django.http import HttpResponse
from my_brew_notifications.models import UserPostNotification


# generates a list of notifications for the current user
def header_notifications_view(request):
    notifications = UserPostNotification.objects.filter(
        user_mentioned__username=request.user.username)
    notification_list = []
    new_notifications = False

    for notification in notifications:
        notification_list.append(notification)
        if notification.viewed is False:
            new_notifications = True
    notification_list.reverse()

    return (notification_list, new_notifications)


# when a notification is viewed the viewed value is turned to true
# using jquery and displays accordingly
def notification_viewed_view(request, notification_id):
    notification = UserPostNotification.objects.get(pk=notification_id)
    notification.viewed = True
    notification.save()

    userNotifications = UserPostNotification.objects.filter(
        user_mentioned__username=request.user.username, viewed=False)
    if userNotifications:
        new_notifications = True
    else:
        new_notifications = False
    return HttpResponse(new_notifications)


# allows the user to delete a notification when they are done with it
def notification_delete_view(request, notification_id):
    notification = UserPostNotification.objects.get(pk=notification_id)
    notification.delete()
    return HttpResponse()
