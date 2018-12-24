$(function () {
    $.ajax({
        url: '/re/note/all/', type: 'post', dataType: 'json', cache: false,
        data: {
            next_id: $('#next_note_id').html()
        },
        success: function (data) {
            $.each(data.set, function (key, value) {
                var appender;
                switch (value.notice_kind) {
                    case 1001:
                        appender = '<div class="note_wrapper">\n' +
                            '<div class="note_img_wrapper">' +
                            '<a href="/' + value.notice_value.username + '/"><img class="note_img_small clickable" src="' + value.notice_value.user_photo + '"></a>' +
                            '</div>\n' +
                            '<div class="note_text_wrapper">' +
                            '<a href="/' + value.notice_value.username + '/"><span class="note_text_username clickable">' + value.notice_value.username + '</span></a>' +
                            'follow you.' +
                            '</div>\n' +
                            '</div>'
                        //follow
                        break;
                    case 2001:
                        appender = '<div class="note_wrapper">\n' +
                            '<div class="note_img_wrapper"><a href="/' + value.notice_value.username + '/"><img class="note_img_small clickable" src="' + value.notice_value.user_photo + '"></a></div>\n' +
                            '<div class="note_text_wrapper"><a href="/' + value.notice_value.username + '/"><span class="note_text_username clickable">' + value.notice_value.username + '</span></a>follow your <a href="/post/' + value.notice_value.post_id + '/"><span class="note_text_post clickable">post</span></a></div>\n' +
                            '</div>'
                        //post_follow
                        break;
                    case 2002:
                        appender = '<div class="note_wrapper">\n' +
                            '<div class="note_img_wrapper"><a href="/' + value.notice_value.username + '/"><img class="note_img_small clickable" src="' + value.notice_value.user_photo + '"></a></div>\n' +
                            '<div class="note_text_wrapper"><a href="/' + value.notice_value.username + '/"><span class="note_text_username clickable">' + value.notice_value.username + '</span></a>comments on <a href="/post/' + value.notice_value.post_id + '/"><span class="note_text_post clickable">post</span></a> - <span class="note_text_detail">' + value.notice_value.comment_text + '</span></div>\n' +
                            '</div>'
                        //post_comment
                        break;
                    case 2003:
                        appender = '<div class="note_wrapper">\n' +
                            '<div class="note_img_wrapper"><a href="/' + value.notice_value.username + '/"><img class="note_img_small clickable" src="' + value.notice_value.user_photo + '"></a></div>\n' +
                            '<div class="note_text_wrapper"><a href="/' + value.notice_value.username + '/"><span class="note_text_username clickable">' + value.notice_value.username + '</span></a>likes <a href="/post/' + value.notice_value.post_id + '/"><span class="note_text_post clickable">post</span></a></div>\n' +
                            '</div>'
                        //post_like
                        break;
                    case 3001:
                        appender = '<div class="note_wrapper">\n' +
                            '<div class="note_img_wrapper"><a href="/' + value.notice_value.username + '/"><img class="note_img_small clickable" src="' + value.notice_value.user_photo + '"></a></div>\n' +
                            '<div class="note_text_wrapper"><a href="/' + value.notice_value.username + '/"><span class="note_text_username clickable">' + value.notice_value.username + '</span></a>likes your post chat on this <a href="/post/' + value.notice_value.post_id + '/"><span class="note_text_post clickable">post</span></a></div>\n' +
                            '</div>'
                        //post_chat_like
                        break;
                    case 4001:
                        appender = '<div class="note_wrapper">\n' +
                            '<div class="note_img_wrapper"><a href="/' + value.notice_value.username + '/"><img class="note_img_small clickable" src="' + value.notice_value.user_photo + '"></a></div>\n' +
                            '<div class="note_text_wrapper"><a href="/' + value.notice_value.username + '/"><span class="note_text_username clickable">' + value.notice_value.username + '</span></a> leave a message on <a href="/post/' + value.notice_value.post_id + '/"><span class="note_text_post clickable">post</span></a> - <span class="note_text_detail">' + value.notice_value.post_chat_rest_text + '</span></div>\n' +
                            '</div>'
                        //post_chat_rest
                        break;
                    case 4002:
                        appender = '<div class="note_wrapper">\n' +
                            '<div class="note_img_wrapper"><a href="/' + value.notice_value.username + '/"><img class="note_img_small clickable" src="' + value.notice_value.user_photo + '"></a></div>\n' +
                            '<div class="note_text_wrapper"><a href="/' + value.notice_value.username + '/"><span class="note_text_username clickable">' + value.notice_value.username + '</span></a>likes your message on <a href="/post/' + value.notice_value.post_id + '/"><span class="note_text_post clickable">post</span></a> - <span class="note_text_detail">' + value.notice_value.post_chat_rest_text + '</span></div>\n' +
                            '</div>'
                        //post_chat_rest_like
                        break;
                    default:
                        break;
                }
                $('#content').append(appender)
            })
            if (data.next === null) {
                $('#more_load').addClass('hidden')
                $('#next_note_id').html('')
            } else {
                $('#more_load').removeClass('hidden')
                $('#next_note_id').html(data.next)
            }

        }
    })
    $('#more_load').click(function (e) {
        e.preventDefault()

        $.ajax({
            url: '/re/note/all/', type: 'post', dataType: 'json', cache: false,
            data: {
                next_id: $('#next_note_id').html()
            },
            success: function (data) {
                $.each(data.set, function (key, value) {
                    var appender;
                    switch (value.notice_kind) {
                        case 1001:
                            appender = '<div class="note_wrapper">\n' +
                                '<div class="note_img_wrapper">' +
                                '<a href="/' + value.notice_value.username + '/"><img class="note_img_small clickable" src="' + value.notice_value.user_photo + '"></a>' +
                                '</div>\n' +
                                '<div class="note_text_wrapper">' +
                                '<a href="/' + value.notice_value.username + '/"><span class="note_text_username clickable">' + value.notice_value.username + '</span></a>' +
                                'follow you.' +
                                '</div>\n' +
                                '</div>'
                            //follow
                            break;
                        case 2001:
                            appender = '<div class="note_wrapper">\n' +
                                '<div class="note_img_wrapper"><a href="/' + value.notice_value.username + '/"><img class="note_img_small clickable" src="' + value.notice_value.user_photo + '"></a></div>\n' +
                                '<div class="note_text_wrapper"><a href="/' + value.notice_value.username + '/"><span class="note_text_username clickable">' + value.notice_value.username + '</span></a>follow your <a href="/post/' + value.notice_value.post_id + '/"><span class="note_text_post clickable">post</span></a></div>\n' +
                                '</div>'
                            //post_follow
                            break;
                        case 2002:
                            appender = '<div class="note_wrapper">\n' +
                                '<div class="note_img_wrapper"><a href="/' + value.notice_value.username + '/"><img class="note_img_small clickable" src="' + value.notice_value.user_photo + '"></a></div>\n' +
                                '<div class="note_text_wrapper"><a href="/' + value.notice_value.username + '/"><span class="note_text_username clickable">' + value.notice_value.username + '</span></a>comments on <a href="/post/' + value.notice_value.post_id + '/"><span class="note_text_post clickable">post</span></a> - <span class="note_text_detail">' + value.notice_value.comment_text + '</span></div>\n' +
                                '</div>'
                            //post_comment
                            break;
                        case 2003:
                            appender = '<div class="note_wrapper">\n' +
                                '<div class="note_img_wrapper"><a href="/' + value.notice_value.username + '/"><img class="note_img_small clickable" src="' + value.notice_value.user_photo + '"></a></div>\n' +
                                '<div class="note_text_wrapper"><a href="/' + value.notice_value.username + '/"><span class="note_text_username clickable">' + value.notice_value.username + '</span></a>likes <a href="/post/' + value.notice_value.post_id + '/"><span class="note_text_post clickable">post</span></a></div>\n' +
                                '</div>'
                            //post_like
                            break;
                        case 3001:
                            appender = '<div class="note_wrapper">\n' +
                                '<div class="note_img_wrapper"><a href="/' + value.notice_value.username + '/"><img class="note_img_small clickable" src="' + value.notice_value.user_photo + '"></a></div>\n' +
                                '<div class="note_text_wrapper"><a href="/' + value.notice_value.username + '/"><span class="note_text_username clickable">' + value.notice_value.username + '</span></a>likes your post chat on this <a href="/post/' + value.notice_value.post_id + '/"><span class="note_text_post clickable">post</span></a></div>\n' +
                                '</div>'
                            //post_chat_like
                            break;
                        case 4001:
                            appender = '<div class="note_wrapper">\n' +
                                '<div class="note_img_wrapper"><a href="/' + value.notice_value.username + '/"><img class="note_img_small clickable" src="' + value.notice_value.user_photo + '"></a></div>\n' +
                                '<div class="note_text_wrapper"><a href="/' + value.notice_value.username + '/"><span class="note_text_username clickable">' + value.notice_value.username + '</span></a> leave a message on <a href="/post/' + value.notice_value.post_id + '/"><span class="note_text_post clickable">post</span></a> - <span class="note_text_detail">' + value.notice_value.post_chat_rest_text + '</span></div>\n' +
                                '</div>'
                            //post_chat_rest
                            break;
                        case 4002:
                            appender = '<div class="note_wrapper">\n' +
                                '<div class="note_img_wrapper"><a href="/' + value.notice_value.username + '/"><img class="note_img_small clickable" src="' + value.notice_value.user_photo + '"></a></div>\n' +
                                '<div class="note_text_wrapper"><a href="/' + value.notice_value.username + '/"><span class="note_text_username clickable">' + value.notice_value.username + '</span></a>likes your message on <a href="/post/' + value.notice_value.post_id + '/"><span class="note_text_post clickable">post</span></a> - <span class="note_text_detail">' + value.notice_value.post_chat_rest_text + '</span></div>\n' +
                                '</div>'
                            //post_chat_rest_like
                            break;
                        default:
                            break;
                    }
                    $('#content').append(appender)

                })
                if (data.next === null) {
                    $('#more_load').addClass('hidden')
                    $('#next_note_id').html('')
                } else {
                    $('#more_load').removeClass('hidden')
                    $('#next_note_id').html(data.next)
                }

            }
        })
    })
})