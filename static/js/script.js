'use strict';


document.addEventListener('DOMContentLoaded', function () {
    document.addEventListener('submit', function (event) {
        if (event.target.classList.contains('delete-post-form')) {
            event.preventDefault();
            const postId = event.target.querySelector('input[name="post_id"]').value;
            deletePost(postId, event.target);
        }
    });
});

function submitPost() {
    const title = document.getElementById('input_title').value;
    const text = document.getElementById('input_textarea').value;
    const photo = document.getElementById('input_img').files[0];

    // Validating data
    if (!title || !text || !photo) {
        displayNotification('Fill everything');
        return;
    }

    const formData = new FormData();
    formData.append('title', title);
    formData.append('photo', photo);
    formData.append('text', text);

    fetch("/post", {
        method: "POST",
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Error posting data");
        }
        return response.json();
    })
    .then(data => {
        displayNotification("Post created successfully!");
        window.location.href = "/posts"; 
    })
    .catch(error => {
        displayNotification("Error creating post.");
        console.error("Error:", error);
    });
}

// Displaying a notification
function displayNotification(message) {
    const notification = document.getElementById("notification");
    notification.innerHTML = message;
}

function deleteAndRedirect(postId) {
    const postIndex = postId - 1; // Adjusting to 0-based indexing

    fetch(`/post/delete`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ post_id: postIndex }) // Sending adjusted postIndex
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error deleting post');
        }
        return response.json();
    })
    .then(data => {
        alert('Post deleted successfully');
        window.location.href = "/posts"; 
    })
    .catch(error => {
        alert('Error deleting post.');
        console.error('Error:', error);
    });
}



// Update the displaySearchResults function in your scripts.js file
function displaySearchResults(results) {
    const usersContainer = $('.con');

    // Clear the current content in the "Users:" section
    usersContainer.html('');

    if (results.length === 0) {
        usersContainer.html('<p>No users found.</p>');
        return;
    }

    // Display search results in the "Users:" section
    results.forEach(post => {
        const postElement = $('<div>').addClass('gen_posts mb-5 text-center');
        postElement.html(`
            <h2>${post.title}</h2>
            ${post.photo ? `<img src="${post.photo}" alt="Post Photo" width="600" class="img-fluid">` : ''}
            <p class="post_text mb-0">${post.text}</p>
        `);
        usersContainer.append(postElement);
    });
}

$(document).ready(function() {
    $('#searchInput').on('input', function() {
        const searchInput = $(this).val();

        $.ajax({
            type: 'POST',
            url: '/search',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({ 'search_term': searchInput }),
            success: function(response) {
                displaySearchResults(response);
            },
            error: function(error) {
                console.error('Error searching for users:', error);
            }
        });
    });
});