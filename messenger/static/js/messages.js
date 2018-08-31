$(function() {
  $("#send").submit(function() {
    var msg_container = $("#msg-container");
    var message_jumbotron = $("div#message_jumbotron");
    $.ajax({
      url: "/messages/send/",
      data: $("#send").serialize(),
      cache: false,
      type: "post",
      success: function(data) {
        $(message_jumbotron).fadeOut("fast");
        $(msg_container).append(data);
        $("input[name='message']").val("");
        $("input[name='message']").focus();
        $(".conversation").scrollTop($(".conversation")[0].scrollHeight);
      }
    });
    return false;
  });
});
