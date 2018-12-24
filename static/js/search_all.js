$(function () {
    if ($('#search_word').html() === '') {
        $('#content_user').append('<div class="h3">No results</div>')
        $('#content_post').append('<div class="h3">No results</div>')
    } else {
        $.ajax({
            url: '/re/search/all/', type: 'post', dataType: 'json', cache: false,
            data: {
                search_word: $('#search_word').html()
            },
            success: function (data) {
                if (data.res === 1) {
                    //post set
                    if (data.post_set.length === 0) {
                        $('#content_post').append('<div class="h3">No results</div>')
                    } else {
                        $.each(data.post_set, function (key, value) {
                            var appender = '<div class="row div_base" id="post_div_' + value.id + '">' +
                                '<script defer>' +
                                '    profile_populate("' + value.id + '")' +
                                '<' + '/script></div>'
                            $('#content_post').append(appender)
                        })
                    }
                    //여기에 모달들 추가해줘야 포스트 작동함. 그 후 모어로드 후 나머지 서치 구현 예
                    if (data.post_next === null) {
                        $('#more_post').addClass('hidden')
                    } else {
                        $('#more_post').removeClass('hidden')
                    }
                    //user set
                    if (data.user_set.length === 0) {
                        $('#content_user').append('<div class="h3">No results</div>')

                    } else {
                        $.each(data.user_set, function (key, value) {
                            var appender = '<div class="search_user_wrapper">\n' +
                                '<div class="search_user_img_wrapper"><a href="/' + value.username + '/"><img class="search_user_img_small clickable" src="' + value.user_photo + '"></a></div>\n' +
                                '<div class="search_user_detail_wrapper"><a href="/' + value.username + '/"><span class="search_user_detail_username clickable">' + value.username + '</span></a><span> <span><a href="/' + value.username + '/"><span class="search_user_detail_name clickable">' + value.user_text_name + '</span></a></div>\n' +
                                '</div>'
                            $('#content_user').append(appender)

                        })
                    }

                    if (data.user_next === null) {
                        $('#more_user').addClass('hidden')
                    } else {
                        $('#more_user').removeClass('hidden')
                    }
                }
            }
        })
    }
})