// Check if there are unread messages
$(document).ready(function() {
  function check_messages() {
    $.ajax({
      url: "/messages/check/",
      cache: false,
      success: function(data) {
        if (data != 0) {
          $("#check_messages span#messages_count").text(data);
        } else {
          $("span#messages_count").remove();
        }
      },
      complete: function() {
        window.setTimeout(check_messages, 60000);
      }
    });
  }
  check_messages();
});
