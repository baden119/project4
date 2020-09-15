document.addEventListener('DOMContentLoaded', function() {

// load all Posts
// load_all_posts();

    // Send Post request to emails route when form submitted
    // document.querySelector('#new-post-form').onsubmit = () => {
    //   fetch('/new_post', {
    //     method: 'POST',
    //     body: JSON.stringify({
    //         body: document.querySelector('#new-post-body').value
    //     })
    //   })
    //   .then(response => response.json())
    //   .then(result => {
    //       console.log(result.message);
    //   })
    //   document.querySelector('#new-post-body').value = '';
    //   return false;
    // };

function load_all_posts(){
  console.log("load all posts!")
  fetch(`/all_posts`)
  .then(response => response.json())
  .then(posts => {
    // Loop through Ajax response and list  info using the list_emails function
    posts.forEach(post =>{

    // Create new post div
    const post_div = document.createElement('div');
    // Inputing email data into mailbox item text
    post_div.innerHTML = `${post.body}`

    // Add mailbox item to DOM
    document.querySelector('#all-posts-view').append(post_div)

      // console.log(post);
    })
  })

};

});
