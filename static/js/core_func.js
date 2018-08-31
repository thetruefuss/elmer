$(document).ready(function() {
  function check_activities() {
    $.ajax({
      url: "/activities/check/",
      cache: false,
      success: function(data) {
        if (data != 0) {
          $("#check_activities span#activities_count").text(data);
        } else {
          $("span#activities_count").remove();
        }
      },
      complete: function() {
        window.setTimeout(check_activities, 60000);
      }
    });
  }
  check_activities();
});
