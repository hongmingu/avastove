$(function () {
    if ($('#search_word').html() === '') {
        $('#content_user').append('<div class="h3">No results</div>')
    } else {
        $.ajax({
            url: '/re/search/user/', type: 'post', dataType: 'json', cache: false,
            data: {
                search_word: $('#search_word').html(),
                next_id: $('#next_id').html()
            },
            success: function (data) {
                if (data.res === 1) {
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
                        $('#more_user_load').addClass('hidden')
                        $('#next_id').html('')
                    } else {
                        $('#more_user_load').removeClass('hidden')
                        $('#next_id').html(data.user_next)
                    }
                }


            }
        })
    }

    $('#more_user_load').on('click', function (e) {
        e.preventDefault()
        $.ajax({
            url: '/re/search/user/', type: 'post', dataType: 'json', cache: false,
            data: {
                search_word: $('#search_word').html(),
                next_id: $('#next_id').html()
            },
            success: function (data) {
                if (data.res === 1) {
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
                        $('#more_user_load').addClass('hidden')
                        $('#next_id').html('')

                    } else {
                        $('#more_user_load').removeClass('hidden')
                        $('#next_id').html(data.user_next)

                    }
                }


            }
        })
    })


})
