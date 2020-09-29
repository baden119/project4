// When page is done loading
document.addEventListener('DOMContentLoaded', function() {

  // Hide all edit boxes
  document.querySelectorAll(".edit_view").forEach(edit_view => {edit_view.style.display = 'none'});

  // When an 'Edit Post' button gets clicked
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
     edit_form_nodes[3].innerHTML = document.querySelector(`#post_body_${this.name}`).innerHTML;

     // When an edited post is submitted
     document.querySelector(`#edit_form_${this.name}`).onsubmit = () => {
       edit_form_nodes = document.querySelector(`#edit_form_${this.name}`).childNodes;

       // Fetch request to server
       fetch('/edit_post', {
         headers: {'X-CSRFToken': document.getElementsByName("csrfmiddlewaretoken")[0].value},
         method: 'POST',
         body: JSON.stringify({
           mode: 'same-origin',
           post_body: edit_form_nodes[3].value,
           post_id: this.name
         }) // body array
       }) //fetch request

       // Dealing with response from server
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

     // When a Cancel button is clicked
     Object.values(document.getElementsByClassName("cancel_button")).forEach(button => {
       button.onclick = function(){
         // Reset the text in the Edit textfield
         edit_form_nodes = document.querySelector(`#edit_form_${this.name}`).childNodes[3].value = saved_text.innerText;
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

 Object.values(document.getElementsByClassName("like_post_button")).forEach(button => {
   button.onclick = function(){

      fetch('/like_post', {
        method: 'POST',
        headers: {'X-CSRFToken': document.getElementsByName("csrfmiddlewaretoken")[0].value},
        body: JSON.stringify({
          post_id: this.name
        }) // body array
      }) //fetch request

      // Dealing with response from server
      .then(response => response.json())
      .then(result => {
        console.log(result);
      })

   }; // like button onclick function
 }); //arrow function for like button


}); //DOMContentLoaded
