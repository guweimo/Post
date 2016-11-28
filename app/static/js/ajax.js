/**
 * Created by lyfw2 on 2016/11/18.
 */


$(function() {
    $("#email").blur(function () {
        if ($("#email").val() != '') {
            $.ajax({
                type: 'POST',
                url: "check_email",
                dataType: "json",
                data: {'email': $("#email").val()},
                success: function (data) {
                    email = $("#email");
                    if (email.next('p').length > 0) {
                        email.next('p').html(data.result);
                    } else {
                        email.parent().append("<p class='help-block'>" + data.result + "</p>");
                    }
                }
            });
        }
    });

    $("#username").blur(function () {
        if ($("#username").val() != '') {
            $.ajax({
                type: 'POST',
                url: "check_email",
                dataType: "json",
                data: {'username': $("#username").val()},
                success: function (data) {
                    username = $("#username");
                    if (username.next('p').length > 0) {
                        username.next('p').html(data.result);
                    } else {
                        username.parent().append("<p class='help-block'>" + data.result + "</p>");
                    }
                }
            });
        }

    });
});