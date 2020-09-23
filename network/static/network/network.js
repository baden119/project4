document.addEventListener('DOMContentLoaded', function() {
// console.log("DO SOMETING!!!!!!!!!!!");
  document.querySelector('#edit_post').onclick = function() {

    const edit_form = document.createElement("FORM");

    const edit_box = document.createElement("INPUT");
    edit_box.type='TEXTAREA';
    edit_box.value = document.querySelector(`#post_body_${this.name}`).innerHTML;
    edit_box.id = "edit_box"

    const submit = document.createElement("INPUT");
    submit.innerHTML = "Save Changes"
    submit.className = "btn btn-primary btn-sm"
    submit.type = "SUBMIT"

    edit_form.appendChild(edit_box);
    edit_form.appendChild(submit);

    document.querySelector(`#post_body_${this.name}`).style.display = 'none';
    document.querySelector(`#edit_box_${this.name}`).append(edit_form);
    // document.querySelector(`#edit_box_${this.name}`).append(submit);

    // document.querySelector('#submit').onclick = function() {
    //   console.log("submit clicked!");
    //
    //   console.log(document.querySelector('#edit_box').innerHTML);

    // };

  };

});
