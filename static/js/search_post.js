$(function () {
    if ($('#search_word').html() === '') {
        $('#content_post').append('<div class="h3">No results</div>')
    } else {
        $.ajax({
            url: '/re/search/post/', type: 'post', dataType: 'json', cache: false,
            data: {
                search_word: $('#search_word').html(),
                next_id: $('#next_id').html()
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
                        $('#more_post_load').addClass('hidden')
                        $('#next_id').html('')
                    } else {
                        $('#more_post_load').removeClass('hidden')
                        $('#next_id').html(data.post_next)
                    }
                    //user set
                }


            }
        })
    }
    $('#more_post_load').on('click', function (e) {
        e.preventDefault()
        $.ajax({
            url: '/re/search/post/', type: 'post', dataType: 'json', cache: false,
            data: {
                search_word: $('#search_word').html(),
                next_id: $('#next_id').html()
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
                        $('#more_post_load').addClass('hidden')
                        $('#next_id').html('')
                    } else {
                        $('#more_post_load').removeClass('hidden')
                        $('#next_id').html(data.post_next)
                    }
                    //user set
                }

            }
        })
    })

})