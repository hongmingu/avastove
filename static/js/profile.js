$(function () {
    $('#post_delete').click(function (e) {
        e.preventDefault()
        $.ajax({
            url: '/re/profile/post/delete/', type: 'post', dataType: 'json', cache: false,
            data: {
                post_id: $('#post_to_delete').html(),
            },
            success: function (data) {
                if (data.res === 1) {
                    $('#post_wrapper_' + $('#post_to_delete').html()).replaceWith('<div>post removed</div>')
                    $('#modal_post_delete').modal('hide')
                }
            }
        })

    })

    $("#modal_post_delete").on("shown.bs.modal", function () {

    }).on("hidden.bs.modal", function () {

        $('#post_to_delete').html('')

    })
});
$(function () {

    $.ajax({
        url: '/re/profile/post/', type: 'post', dataType: 'json', cache: false,
        data: {
            chosen_user_id: $('#chosen_user_id').html(),
            last_post_id: $('#last_post_id').html()
        },
        success: function (data) {
            var _modifier = ''
            $.each(data.set, function (key, value) {

                if (data.master === true) {
                    _modifier = '<div align="right"><a href="/post/update/' + value.id + '/"><span class="profile_update">update</span></a><span>  </span><a href=""><span class="profile_delete">delete</span></a></div>'
                }
                var appender = '<div id="post_wrapper_' + value.id + '"><div class="row div_base profile_post_div" id="post_div_' + value.id + '">' +
                    '<script defer>' +
                    '    profile_populate("' + value.id + '")' +
                    '<' + '/script></div>' + _modifier + '</div>'
                var jq_appender = $(appender)
                jq_appender.find('.profile_delete').on('click', function (e) {
                    e.preventDefault()
                    $('#post_to_delete').html(value.id)
                    $('#modal_post_delete').modal('show')
                })
                $('#post_list').append(jq_appender)
            })
            if (data.last === null) {
                $('#profile_more_load').addClass('hidden')
                $('#last_post_id').html('')
            } else {
                $('#profile_more_load').removeClass('hidden')
                $('#last_post_id').html(data.last)
            }

        }
    })

    $('#profile_more_load').click(function (e) {
        e.preventDefault()
        $.ajax({
            url: '/re/profile/post/', type: 'post', dataType: 'json', cache: false,
            data: {
                chosen_user_id: $('#chosen_user_id').html(),
                last_post_id: $('#last_post_id').html()
            },
            success: function (data) {
                var _modifier = ''
                $.each(data.set, function (key, value) {

                    if (data.master === true) {
                        _modifier = '<div align="right"><a href="/post/update/' + value.id + '/"><span class="profile_update">update</span></a><span>  </span><a href=""><span class="profile_delete">delete</span></a></div>'
                    }
                    var appender = '<div id="post_wrapper_' + value.id + '"><div class="row div_base profile_post_div" id="post_div_' + value.id + '">' +
                        '<script defer>' +
                        '    profile_populate("' + value.id + '")' +
                        '<' + '/script></div>' + _modifier + '</div>'
                    var jq_appender = $(appender)
                    jq_appender.find('.profile_delete').on('click', function (e) {
                        e.preventDefault()
                        $('#post_to_delete').html(value.id)
                        $('#modal_post_delete').modal('show')
                    })
                    $('#post_list').append(jq_appender)
                })
                if (data.last === null) {
                    $('#profile_more_load').addClass('hidden')
                    $('#last_post_id').html('')

                } else {
                    $('#profile_more_load').removeClass('hidden')
                    $('#last_post_id').html(data.last)
                }

            }
        })
    })
})

$(function () {
    var height = $(window).height();
    $('.modal_follow_wrapper').css('max-height', height - 120);
    $(window).on('resize', function () {
        if ($(window).height() != height) {
            height = $(window).height();
            $('.modal_follow_wrapper').css('max-height', height - 120);
        }
    });
})
$(function () {
    if ($('#user_id').html() === $('#chosen_user_id').html()) {
        $('#follow').addClass('hidden')
    } else {
        $('#follow').removeClass('hidden')
    }
    $('#follow').click(function (e) {
        e.preventDefault()
        if ($('#user_id').html() === '') {
            $('#modal_need_login').modal('show')
            return false;
        }
        $.ajax({
            url: '/re/profile/follow/', type: 'post', dataType: 'json', cache: false,
            data: {
                user_id: $('#chosen_user_id').html()
            },
            success: function (data) {
                if (data.result === true) {
                    $('#follow_text').html('following <span class="glyphicon glyphicon-ok"></span>')
                    var count_follower = parseInt($('#count_follower').html()) + 1
                    $('#count_follower').html(count_follower)
                } else {
                    $('#follow_text').html('follow')
                    var count_follower = parseInt($('#count_follower').html()) - 1
                    $('#count_follower').html(count_follower)
                }
            }
        })
    })

    $("#modal_following").on("shown.bs.modal", function () {
        var height = $(window).height();
        $('.modal_follow_wrapper').css('max-height', height - 120);
        $(window).on('resize', function () {

            if ($(window).height() != height) {
                height = $(window).height();
                $('.modal_follow_wrapper').css('max-height', height - 120);
            }
        });
        var chosen_user_id = $('#chosen_user_id').html()

        $.ajax({
            url: '/re/profile/following/', type: 'post', dataType: 'json', cache: false,
            data: {
                user_id: $('#chosen_user_id').html(),
                next_id: $('#next_id').html()
            },
            success: function (data) {
                if (data.res === 1) {
                    $.each(data.set, function (key, value) {
                        var appender = '<div class="profile_list_wrapper"><a href="/' + value.username + '/">\n' +
                            '<img class="img_small" src="' + value.photo + '">\n' +
                            '<span class="profile_list_username">' + value.username + '</span>\n' +
                            '</a></div>'
                        $('#modal_following_list').append(appender)
                    })
                }
                if (data.next === null) {
                    $('#next_id').html('')
                    $('#modal_following_more').addClass('hidden')
                } else {
                    $('#next_id').html(data.next)
                    $('#modal_following_more').removeClass('hidden')
                }

            }
        })
    }).on("hidden.bs.modal", function () {
        $('#modal_following_list').empty()
        $('#next_id').html('')
    });

    $('#modal_following_more').click(function (e) {
        e.preventDefault()
        var chosen_user_id = $('#chosen_user_id').html()

        $.ajax({
            url: '/re/profile/following/', type: 'post', dataType: 'json', cache: false,
            data: {
                user_id: $('#chosen_user_id').html(),
                next_id: $('#next_id').html()
            },
            success: function (data) {
                if (data.res === 1) {
                    $.each(data.set, function (key, value) {
                        var appender = '<div class="profile_list_wrapper"><a href="/' + value.username + '/">\n' +
                            '<img class="img_small" src="' + value.photo + '">\n' +
                            '<span class="profile_list_username">' + value.username + '</span>\n' +
                            '</a></div>'
                        $('#modal_following_list').append(appender)
                    })
                }
                if (data.next === null) {
                    $('#next_id').html('')
                    $('#modal_following_more').addClass('hidden')
                } else {
                    $('#next_id').html(data.next)
                    $('#modal_following_more').removeClass('hidden')
                }

            }
        })
    })

    $('#count_following').click(function (e) {
        $('#modal_following').modal('show')
    })


    $("#modal_follower").on("shown.bs.modal", function () {

        var height = $(window).height();
        $('.modal_follow_wrapper').css('max-height', height - 120);
        $(window).on('resize', function () {

            if ($(window).height() != height) {
                height = $(window).height();
                $('.modal_follow_wrapper').css('max-height', height - 120);
            }
        });
        var chosen_user_id = $('#chosen_user_id').html()

        $.ajax({
            url: '/re/profile/follower/', type: 'post', dataType: 'json', cache: false,
            data: {
                user_id: $('#chosen_user_id').html(),
                next_id: $('#next_id').html()
            },
            success: function (data) {
                if (data.res === 1) {
                    $.each(data.set, function (key, value) {
                        var appender = '<div class="profile_list_wrapper"><a href="/' + value.username + '/">\n' +
                            '<img class="img_small" src="' + value.photo + '">\n' +
                            '<span class="profile_list_username">' + value.username + '</span>\n' +
                            '</a></div>'
                        $('#modal_follower_list').append(appender)
                    })
                }
                if (data.next === null) {
                    $('#next_id').html('')
                    $('#modal_follower_more').addClass('hidden')
                } else {
                    $('#next_id').html(data.next)
                    $('#modal_follower_more').removeClass('hidden')
                }

            }
        })
    }).on("hidden.bs.modal", function () {
        $('#modal_follower_list').empty()
        $('#next_id').html('')
    });

    $('#modal_follower_more').click(function (e) {
        e.preventDefault()
        var chosen_user_id = $('#chosen_user_id').html()

        $.ajax({
            url: '/re/profile/follower/', type: 'post', dataType: 'json', cache: false,
            data: {
                user_id: $('#chosen_user_id').html(),
                next_id: $('#next_id').html()
            },
            success: function (data) {
                if (data.res === 1) {
                    $.each(data.set, function (key, value) {
                        var appender = '<div class="profile_list_wrapper"><a href="/' + value.username + '/">\n' +
                            '<img class="img_small" src="' + value.photo + '">\n' +
                            '<span class="profile_list_username">' + value.username + '</span>\n' +
                            '</a></div>'
                        $('#modal_follower_list').append(appender)
                    })
                }
                if (data.next === null) {
                    $('#next_id').html('')
                    $('#modal_follower_more').addClass('hidden')
                } else {
                    $('#next_id').html(data.next)
                    $('#modal_follower_more').removeClass('hidden')
                }

            }
        })
    })

    $('#count_follower').click(function (e) {
        $('#modal_follower').modal('show')
    })
})
