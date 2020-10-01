// When page is done loading
document.addEventListener('DOMContentLoaded', function() {

  // Hide all edit boxes
  document.querySelectorAll(".edit_view").forEach(edit_view => {edit_view.style.display = 'none'});

  // When an 'Edit Post' button is clicked:
   Object.values(document.getElementsByClassName("edit_post_button")).forEach(button => {
     button.onclick = function(){

    // Disable all edit buttons on page.
    Object.values(document.getElementsByClassName("edit_post_button")).forEach(button => {
      button.disabled = true;
    });

     // Hide selected post and show selected edit box.
     document.querySelector(`#post_body_${this.name}`).style.display = 'none';
     document.querySelector(`#edit_view_${this.name}`).style.display = 'block';

     // Populate edit box with text of selected post
     let saved_text = document.querySelector(`#post_body_${this.name}`)
     edit_form_nodes = document.querySelector(`#edit_form_${this.name}`).childNodes;
     console.log(document.querySelector(`#post_body_${this.name}`).innerHTML);
     console.log(edit_form_nodes);
     edit_form_nodes[1].innerHTML = document.querySelector(`#post_body_${this.name}`).innerHTML;

     // When an edited post is submitted:
     document.querySelector(`#edit_form_${this.name}`).onsubmit = () => {
       edit_form_nodes = document.querySelector(`#edit_form_${this.name}`).childNodes;

       // Fetch request to /edit_post route containing new post text
       fetch('/edit_post', {
         headers: {'X-CSRFToken': document.getElementsByName("csrfmiddlewaretoken")[0].value},
         method: 'POST',
         body: JSON.stringify({
           mode: 'same-origin',
           post_body: edit_form_nodes[1].value,
           post_id: this.name
         }) // body array
       }) //fetch request

       // Populate the post body field in HTML with post data recieved from server.
       // Also hide the edit box and show the post body field.
       .then(response => response.json())
       .then(result => {
         document.querySelector(`#post_body_${this.name}`).innerHTML = result.post_body;
         document.querySelector(`#post_body_${this.name}`).style.display = 'block';
         document.querySelector(`#edit_view_${this.name}`).style.display = 'none';
       })
       //Re-enable Edit buttons
       Object.values(document.getElementsByClassName("edit_post_button")).forEach(button => {
         button.disabled = false;
       });
       // Disabling standard submission behaviour
       return false;
     };// edit post form onsubmit

     // When a Cancel button is clicked:
     Object.values(document.getElementsByClassName("cancel_button")).forEach(button => {
       button.onclick = function(){
         // Reset the text in the Edit textfield
         document.querySelector(`#edit_form_${this.name}`).childNodes[3].value = saved_text.innerText;
         // Hide Edit textfield and display regular Post view
         document.querySelector(`#post_body_${this.name}`).style.display = 'block';
         document.querySelector(`#edit_view_${this.name}`).style.display = 'none';
         //Re-enable Edit buttons
         Object.values(document.getElementsByClassName("edit_post_button")).forEach(button => {
           button.disabled = false;
         });

       }; // cancel button onclick function
     }); //arrow function for cancel

   }; //edit button onclick function
 }); //arrow function for edit

// When a Like button gets clicked:
 Object.values(document.getElementsByClassName("like_post_button")).forEach(button => {
   button.onclick = function(){

      // Fetch request to /like_post route containing post's id.
      fetch('/like_post', {
        method: 'POST',
        headers: {'X-CSRFToken': document.getElementsByName("csrfmiddlewaretoken")[0].value},
        body: JSON.stringify({
          post_id: this.name
        }) // body arraylike_count.innerHTML
      }) //fetch request

      // Dealing with response from server
      .then(response => response.json())
      .then(result => {
        console.log(result);

        // Update Post's like count with data from server
        document.querySelector(`#like_count_${this.name}`).innerHTML = result.like_count;

        // Toggle button between 'Like' and 'Liked' based on data recieved from server.
        if (result.like_condition === true){
          document.querySelector(`#like_button_${this.name}`).innerHTML = " &#128151; Liked &#128151; ";
        }
        if (result.like_condition === false){
          document.querySelector(`#like_button_${this.name}`).innerHTML = " &#9825; Like &#9825; ";
        }
      }) //.then(result) arrow function

   }; // like button onclick function
 }); //arrow function for like button


}); //DOMContentLoaded
