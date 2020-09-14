document.addEventListener('DOMContentLoaded', function() {

  console.log("DO sOMETHING!");

    // Send Post request to emails route when form submitted
    document.querySelector('#new-post-form').onsubmit = () => {

      console.log(document.querySelector('#new-post-body').value)
      console.log("FOrm Submitted!")
      fetch('/new_post', {
        method: 'POST',
        body: JSON.stringify({
            body: document.querySelector('#new-post-body').value
        })
      })
      .then(response => response.json())
      .then(result => {
          console.log(result.message);
      })
      document.querySelector('#new-post-body').value = '';
      return false;
    };


});
