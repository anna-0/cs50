document.addEventListener('DOMContentLoaded', function() {

    // Cannot post empty form
    const submit = document.querySelector('#addpost');
    const post_text = document.querySelector('#post-text');

    if (submit) {
        submit.disabled = true;
        post_text.onkeyup = () => {
            if (post_text.value.length > 0) {
                submit.disabled = false;
            }
            else {
                submit.disabled = true;
            }
        }    
    }

    const postForm = document.querySelector('#post-form');

    // Add post
    if (postForm) {
        postForm.addEventListener('submit', () => add_post());
    }

    // Like post
    document.addEventListener('click', (event) => {
        let element = event.target;
        if (element.classList.contains('like-button')) {
            toggleLike(element);
        }
        else if (element.id == 'follow') {
            toggleFollow(element.dataset.user);
        }
    }); 
});

function add_post() {
    
    fetch('/add-post', {
        method: 'POST',
        body: JSON.stringify({
            body: document.querySelector('#post-text').value,
        })
    })
    .then(response => response.json())
    .then(result => {
        // Error alert
        if (result['error']) {
            alert(result['error']);
        }
        else {
            console.log('Posted');
        }
    });
    return false; 
}

function editPost(post) {

    post.parentElement.children[1].style.display = 'none';
    post.parentElement.children[2].style.display = 'block';
    return false;
}

function saveEdit(el) {

    text = el.parentElement.children[0].value;
    id = el.dataset.id;
    post = el.parentElement.parentElement.children[1];

    fetch(`/post/${id}`, {
        method: 'PATCH',
        body: JSON.stringify({
            body: text,
        })
    })
    .then(response => response.json())
    .then((response) => {
        post.textContent = text;
        post.style.display = 'block';
        el.parentElement.parentElement.children[2].style.display = 'none';
    })
    .catch((response) => {
        alert('Error');
    });
    return false;
}

function toggleLike(likeButton) {
    const user_id = JSON.parse(document.getElementById('user-id').textContent);
    const post_id = likeButton.dataset.id;
    let likesCount = likeButton.parentElement.children[4].children[0];

    fetch('/like', {
        method: 'PUT',
        body: JSON.stringify({
          user_id,
          post_id,
        }),
      })
      .then(response => response.json())
        .then((response) => {
            
          if (likesCount.dataset.is_liked == 'yes') {
            likesCount.setAttribute('data-is_liked', 'no');
            likeButton.innerHTML = '👍 Like';
            likesCount.innerHTML = parseInt(likesCount.textContent) - 1;
          }
          else if (likesCount.dataset.is_liked == 'no') {
            likesCount.setAttribute('data-is_liked', 'yes')
            likeButton.innerHTML = '👎 Unlike';
            likesCount.innerHTML = parseInt(likesCount.textContent) + 1;
          }
        })
        .catch((response) => {
            alert('Error');
        });
        return false;
    }

function toggleFollow(user) {
    const current = JSON.parse(document.getElementById('current-id').textContent);
    let user_id = parseInt(user);
    const followButton = document.querySelector('#follow');
    let followerCount = document.querySelector('#followerCount');

    fetch('/follow', {
        method: 'PUT',
        body: JSON.stringify({
            current,
            user_id,
        }),
    })
    .then(response => response.json())
    .then((response) => {
        if (response.message == 'Followed') {
            followButton.innerHTML = 'Unfollow';
            followButton.className = 'btn btn-danger';
            followerCount.innerHTML = parseInt(followerCount.textContent) + 1;
        }
        else if (response.message == 'Unfollowed') {
            followButton.innerHTML = 'Follow';
            followButton.className = 'btn btn-success';
            followerCount.innerHTML = parseInt(followerCount.textContent) - 1;
        }
    })
    .catch((response) => {
        alert('Error');
    });
    return false;
}