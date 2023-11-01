function getUserId() {
  // Retrieve the user_id from the session variable
  var user_id = document.body.getAttribute("data-user-id");
  return user_id;
}
