document.addEventListener('DOMContentLoaded', function() {

  document.querySelectorAll(".edit_view").forEach(edit_view => {
                    edit_view.style.display = 'none';
                });

  document.querySelector('#edit_post').onclick = function() {

    document.querySelector('#edit_post').disabled = true;

    document.querySelector(`#post_body_${this.name}`).style.display = 'none';
    document.querySelector(`#edit_view_${this.name}`).style.display = 'block';

    edit_form_nodes = document.querySelector(`#edit_form_${this.name}`).childNodes;

    edit_form_nodes[3].innerHTML = document.querySelector(`#post_body_${this.name}`).innerHTML;

    document.querySelector(`#edit_form_${this.name}`).onsubmit = () => {
      console.log("submit clicked!!")
      edit_form_nodes = document.querySelector(`#edit_form_${this.name}`).childNodes;

      const csrftoken = edit_form_nodes[1].value;

      fetch('/edit_post', {
        headers: {'X-CSRFToken': csrftoken},
        method: 'POST',
        body: JSON.stringify({
          mode: 'same-origin',
          post_body: edit_form_nodes[3].value,
          post_id: this.name
          }) // body
      }) //fetch request
      .then(response => response.json())
      .then(result => {
        console.log(result);
      }) //result
      return false;
  }; //edit_form.onsubmit

  // function getCookie(name) {
  //     let cookieValue = null;
  //     if (document.cookie && document.cookie !== '') {
  //         const cookies = document.cookie.split(';');
  //         for (let i = 0; i < cookies.length; i++) {
  //             const cookie = cookies[i].trim();
  //             // Does this cookie string begin with the name we want?
  //             if (cookie.substring(0, name.length + 1) === (name + '=')) {
  //                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
  //                 break;
  //             }
  //         }
  //     }
  //     console.log("cookie function about to return")
  //     console.log(cookieValue)
  //     return cookieValue;
  // } // getcookie function

}; // edit_post.onclick

}); //DOMContentLoaded
