$(function () {

$("#modal_feed_menu").on("shown.bs.modal", function () {
        var clicked_post = $('#clicked_post_id').html()
        var scheme = window.location.protocol == "https:" ? "https" : "http";
        var path = scheme + '://' + window.location.host + '/post/' + clicked_post;
        $('#modal_feed_input').val(path).select();
    }).on("hidden.bs.modal", function () {
        $('#clicked_post_id').html('')
        $('#modal_feed_input').val('')
    });

    $('#modal_feed_menu_copy').click(function (e) {
        e.preventDefault()
        var clicked_post = $('#clicked_post_id').html()
        var scheme = window.location.protocol == "https:" ? "https" : "http";
        var path = scheme + '://' + window.location.host + '/post/' + clicked_post;
        $('#modal_feed_input').val(path).select();
        document.execCommand('Copy')
    })
    $('#modal_feed_menu_locate').click(function (e) {
        e.preventDefault()
        var clicked_post = $('#clicked_post_id').html()
        var scheme = window.location.protocol == "https:" ? "https" : "http";
        var path = scheme + '://' + window.location.host + '/post/' + clicked_post;
        location.href=path
    })
})