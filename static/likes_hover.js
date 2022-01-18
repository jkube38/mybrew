function displayLikes (id) {
    elementId = `drop${id}`
    let likes = document.getElementById(elementId)
        likes.style.display = 'flex'
        likes.style.flexDirection = 'column'
}

function hideLikes (id) {
    elementId = `drop${id}`
    let likes = document.getElementById(elementId)
        likes.style.display = 'none'
}

// onmouseover="displayLikes({{ post.0.id }})" onmouseout="hideLikes({{ post.0.id }})"