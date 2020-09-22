document.addEventListener('DOMContentLoaded', function() {

console.log("DO SOMEEEETHING!!!")

document.querySelector('#edit_post').onclick = function() {
  console.log("EDIT POST CLICKED!!!")

  document.querySelector('#post_body').style.color = 'red';

  // const body = document.querySelector('#post_body').value;
  //
  // console.log(body)
};




});
