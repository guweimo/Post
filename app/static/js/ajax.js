/**
 * Created by lyfw2 on 2016/11/18.
 */




$(function () {
    // $(".profile-header .btn").bind('click', function () {
    //     $.get("/follow/1", function (data) {
    //         if (data.bol) {
    //             $(".profile-header .btn").removeClass("btn-primary");
    //             $(".profile-header .btn").addClass("btn-default");
    //             $(".profile-header .btn").text("取消关注");
    //         } else {
    //             $(".profile-header .btn").removeClass("btn-default");
    //             $(".profile-header .btn").addClass("btn-primary");
    //             $(".profile-header .btn").text("关注");
    //         }
    //     });
    // });
    $(".profile-header .btn").bind('click', function () {
        $.ajax({
            url: '/follow/1',
            dataType: 'json',
            data: null,
            contentType: "application/json;charset=utf-8",
            success: function (data) {
                if (data.bol) {
                    $(".profile-header .btn").removeClass("btn-primary");
                    $(".profile-header .btn").addClass("btn-default");
                    $(".profile-header .btn").text("取消关注");
                } else {
                    $(".profile-header .btn").removeClass("btn-default");
                    $(".profile-header .btn").addClass("btn-primary");
                    $(".profile-header .btn").text("关注");
                }
                $(".badge:first").text(data.count);
            },
            error: function (result) {
                alert(result.status + "：" + result.statusText);
            }
        });
    });
});