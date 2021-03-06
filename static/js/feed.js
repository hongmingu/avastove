$(function () {
    $.ajax({
        url: '/re/explore/feed/', type: 'post', dataType: 'json', cache: false,
        data: {
            last_id: $('#post_last_id').html()
        },
        success: function (data) {
            $.each(data.set, function (key, value) {
                var string = value.id
                var appender = '<div class="row div_base" id="post_div_' + value.id + '">' +
                    '<script defer>' +
                    '    home_populate("' + value.id + '")' +
                    '<' + '/script></div>'
                $('#content').append(appender)
                $('#post_last_id').html(value.id)
            })
            if (data.last === null) {
                $('#home_feed_more_load').addClass('hidden')
            } else {
                $('#home_feed_more_load').removeClass('hidden')
            }

        }
    })
    $('#more_load').click(function (e) {
        e.preventDefault()
        $.ajax({
            url: '/re/explore/feed/', type: 'post', dataType: 'json', cache: false,
            data: {
                last_id: $('#post_last_id').html()
            },
            success: function (data) {
                $.each(data.set, function (key, value) {
                    var string = value.id
                    var appender = '<div class="row div_base" id="post_div_' + value.id + '">' +
                        '<script defer>' +
                        '    home_populate("' + value.id + '")' +
                        '<' + '/script></div>'
                    $('#content').append(appender)
                    $('#post_last_id').html(value.id)
                })
                if (data.last === null) {
                    $('#home_feed_more_load').addClass('hidden')
                } else {
                    $('#home_feed_more_load').removeClass('hidden')
                }

            }
        })
    })
})
