function displayNotifications () {
    let notify = document.getElementById('notifications')
        notify.style.display = 'flex'
        notify.style.flexDirection = 'column'
        notify.style.zIndex = '1'
}

function hideNotifications () {
    let notify = document.getElementById('notifications')
        notify.style.display = 'none'
}
