// When page is done loading
document.addEventListener('DOMContentLoaded', function() {

  // Hide all edit boxes
  document.querySelectorAll(".edit_view").forEach(edit_view => {edit_view.style.display = 'none'});

  // When an 'Edit Post' button gets clicked
  console.log("function start")

  let edit_buttons = document.getElementsByClassName("edit_post_button");

  for (var i = 0; i < edit_buttons.length; i++) {
     edit_buttons.item(i).onclick = function(){

    // Implement a cancel button which is hidden on load but which apears when edit
    // gets clicked, this button will just undo the display changes and maybe change
    // the value of the edit form to nothing. I'd also like another for loop disabling
    // all other edit buttons once one has been clicked, but this will probably require
    // another for loop re-enableing them all once form is submitted or edit is cancelled.

     // // Disable edit button, hide selected post and show selected edit box
     // document.querySelector('#edit_post').disabled = true;
     document.querySelector(`#post_body_${this.name}`).style.display = 'none';
     document.querySelector(`#edit_view_${this.name}`).style.display = 'block';

     // Populate edit box with text of selected post
     edit_form_nodes = document.querySelector(`#edit_form_${this.name}`).childNodes;
     edit_form_nodes[3].innerHTML = document.querySelector(`#post_body_${this.name}`).innerHTML;

     // When an edited post is submitted
     document.querySelector(`#edit_form_${this.name}`).onsubmit = () => {
       console.log("submit clicked!!")
       edit_form_nodes = document.querySelector(`#edit_form_${this.name}`).childNodes;

       // Accessing csrf token
       const csrftoken = edit_form_nodes[1].value;

       // Fetch request to server
       fetch('/edit_post', {
         headers: {'X-CSRFToken': csrftoken},
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
         console.log(result);
       })

       // Disabling standard submission behaviour
       return false;
     };// edit post form onsubmit
   }; //edit button onclick function
 }; //edit button for loop
  console.log("function end");
}); //DOMContentLoaded
