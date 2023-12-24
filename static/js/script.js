// document.addEventListener('DOMContentLoaded', function() {
//     // Fetch posts data
//     fetch('/posts')
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok');
//             }
//             return response.json();
//         })
//         .then(posts => {
//             // Process received posts data
//             posts.forEach(function(post) {
//                 let card = $('<div>').addClass("card mt-3");
//                 if (post.filename) {
//                     let imgElement = $("<img>").addClass("card-img-top").attr("src", post.filename).attr("alt", "Image description");
//                     card.append(imgElement);
//                 }
//                 let cardBody = $('<div>').addClass('card-body');
//                 card.append(cardBody);

//                 if (post.title) {
//                     let titleElement = $("<h5>").addClass("card-title").text(post.title);
//                     cardBody.append(titleElement);
//                 }
//                 if (post.content) {
//                     let contentElement = $("<h6>").addClass("card-content").text(post.content);
//                     cardBody.append(contentElement);
//                 }
//                 $("#wall").append(card);
//             });
//         })
//         .catch(error => {
//             console.error("Error", error);
//         });

//     // Event listener for form submission
//     document.querySelector('#postForm').addEventListener('submit', function(event) {
//         event.preventDefault();
//         var fileInput = document.getElementById('postFile').files[0];
//         var postTitle = document.getElementById('postTitle').value;
//         var postContent = document.getElementById('postText').value;
//         var formData = new FormData();

//         formData.append('file', fileInput);
//         formData.append('title', postTitle);
//         formData.append('content', postContent);

//         fetch('/posts/create_post', {
//                 method: 'POST',
//                 body: formData
//             })
//             .then(response => {
//                 if (!response.ok) {
//                     throw new Error('Error creating post');
//                 }
//                 document.getElementById('postTitle').value = "";
//                 document.getElementById('postFile').value = "";
//                 document.getElementById('postText').value = "";
//                 return response.json();
//             })
//             .then(post => {
//                 console.log("Received post data:", post);
//                 let card = $('<div>').addClass('card mt-3');

//                 if (post.filename) {
//                     let imgElement = $('<img>').addClass('card-img-top').attr("src", post.filename).attr("alt", "Image description");
//                     card.append(imgElement);
//                 }
//                 let cardBody = $('<div>').addClass('card-body');
//                 card.append(cardBody);

//                 if (post.title) {
//                     let titleElement = $("<h5>").addClass('card-title').text(post.title);
//                     cardBody.append(titleElement);
//                 }
//                 if (post.content) {
//                     let contentElement = $('<h6>').addClass('card-content').text(post.content);
//                     cardBody.append(contentElement);
//                 }

//                 $('#wall').append(card);
//             })
//             .catch(error => {
//                 console.error('Error post', error);
//             });
//     });
// });