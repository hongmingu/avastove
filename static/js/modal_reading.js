$(function () {
    $("#modal_reading_post").on("shown.bs.modal", function () {

        var height = $(window).height();
        $('#modal_reading_post_content').css('height', height - 16);
        $('#modal_reading_chat').css('height', height - 16 - 70 - 35 - 30)

        var reading_post_id = $('#reading_post_id').html()
        var reading_post_profile_photo = $('#reading_post_profile_photo').html()
        var reading_post_profile_name = $('#reading_post_profile_name').html()
        $.ajax({
            url: '/re/post/already/read/', type: 'post', dataType: 'json', cache: false,
            data: {
                post_id: reading_post_id,
            },
            success: function (data) {
                if (data.res === 1) {
                    var start = false
                    $.each(data.set, function (key, value) {
                        if (key === 0) {
                            $('#reading_post_chat_last_id').html(value.id)
                        }
                        $('#reading_post_chat_before_id').html(value.id)
                        var prepender;

                        var align, profile_photo, chat_content, like, like_count, rest_messages;
                        switch (value.kind) {
                            case 'start':
                                start = true
                                if (value.rest_count === 0) {
                                    rest_messages = ''
                                } else if (value.rest_count < 1000) {
                                    rest_messages = '<div id="rest_wrapper_' + value.id + '"><a href=""><div class="reading_chat_rest_messages clickable" id="rest_start_' + value.id + '" data-u="' + value.id + '" align="center">' + value.rest_count + ' messages</div></a></div><a href=""><div id="rest_more_' + value.id + '" class="rest_more_load reading_chat_rest_messages hidden" data-u="' + value.id + '" align="center">more</div></a><div class="hidden" id="rest_last_' + value.id + '"></div>'
                                } else if (1000 <= value.rest_count) {
                                    rest_messages = '<div id="rest_wrapper_' + value.id + '"><a href=""><div class="reading_chat_rest_messages clickable" id="rest_start_' + value.id + '" data-u="' + value.id + '" align="center">' + parseInt(value.like_count / 1000) + 'k' + ' messages</div></a></div><a href=""><div id="rest_more_' + value.id + '" class="rest_more_load reading_chat_rest_messages hidden" data-u="' + value.id + '" align="center">more</div></a><div class="hidden" id="rest_last_' + value.id + '"></div>'
                                }
                                prepender = $(rest_messages)
                                break;
                            case 'text':
                                if (value.you_say === true) {
                                    like_count = value.like_count

                                    var heart;
                                    if (value.you_like === true) {
                                        heart = 'glyphicon-heart'
                                    } else {
                                        heart = 'glyphicon-heart-empty'
                                    }
                                    like = '<a href=""><span class="glyphicon ' + heart + ' reading_like" id="reading_like_span_' + value.id + '" data-u="' + value.id + '"></span></a><span class="reading_like_text"> </span><a href=""><span class="reading_like_text" id="reading_like_count_' + value.id + '">' + like_count + '</span></a>'

                                    chat_content = '<div class="reading_chat_content_i">' +
                                        '<div>' + value.content + like + '</div>' +
                                        '</div>'

                                    if (value.rest_count === 0) {
                                        rest_messages = ''
                                    } else {
                                        rest_messages = '<div id="rest_wrapper_' + value.id + '"><a href=""><div class="reading_chat_rest_messages clickable" id="rest_start_' + value.id + '" data-u="' + value.id + '" align="center">' + value.rest_count + ' messages</div></a></div><a href=""><div id="rest_more_' + value.id + '" class="rest_more_load reading_chat_rest_messages hidden" data-u="' + value.id + '" align="center">more</div></a><div class="hidden" id="rest_last_' + value.id + '"></div>'
                                    }

                                    prepender = $('<div>' + chat_content + rest_messages + '</div>')

                                } else if (value.you_say === false) {
                                    like_count = value.like_count

                                    var heart;
                                    if (value.you_like === true) {
                                        heart = 'glyphicon-heart'
                                    } else {
                                        heart = 'glyphicon-heart-empty'
                                    }
                                    like = '<a href=""><span class="glyphicon ' + heart + ' reading_like" id="reading_like_span_' + value.id + '" data-u="' + value.id + '"></span></a><span class="reading_like_text"> </span><a href=""><span class="reading_like_text" id="reading_like_count_' + value.id + '">' + like_count + '</span></a>'

                                    chat_content = '<div class="reading_chat_content_someone">' +
                                        '<div>' + value.content + like + '</div>' +
                                        '</div>'

                                    if (value.rest_count === 0) {
                                        rest_messages = ''
                                    } else {
                                        rest_messages = '<div id="rest_wrapper_' + value.id + '"><a href=""><div class="reading_chat_rest_messages clickable" id="rest_start_' + value.id + '" data-u="' + value.id + '" align="center">' + value.rest_count + ' messages</div></a></div><a href=""><div id="rest_more_' + value.id + '" class="rest_more_load reading_chat_rest_messages hidden" data-u="' + value.id + '" align="center">more</div></a><div class="hidden" id="rest_last_' + value.id + '"></div>'
                                    }

                                    prepender = $('<div>' + chat_content + rest_messages + '</div>')


                                }

                                break;

                            case 'photo':

                                if (value.you_say === true) {

                                    like_count = value.like_count

                                    var heart;
                                    if (value.you_like === true) {
                                        heart = 'glyphicon-heart'
                                    } else {
                                        heart = 'glyphicon-heart-empty'
                                    }
                                    like = '<a href=""><span class="glyphicon ' + heart + ' reading_like" id="reading_like_span_' + value.id + '" data-u="' + value.id + '"></span></a><span class="reading_like_text"> </span><a href=""><span class="reading_like_text" id="reading_like_count_' + value.id + '">' + like_count + '</span></a>'

                                    if (value.rest_count === 0) {
                                        rest_messages = ''
                                    } else {
                                        rest_messages = '<div id="rest_wrapper_' + value.id + '"><a href=""><div class="reading_chat_rest_messages clickable" id="rest_start_' + value.id + '" data-u="' + value.id + '" align="center">' + value.rest_count + ' messages</div></a></div><a href=""><div id="rest_more_' + value.id + '" class="rest_more_load reading_chat_rest_messages hidden" data-u="' + value.id + '" align="center">more</div></a><div class="hidden" id="rest_last_' + value.id + '"></div>'
                                    }

                                    chat_content = '<div class="reading_chat_content_i">' +
                                        '<div><img class="reading_chat_img" src="' + value.content + '">' + like + '</div>' +
                                        '</div>'
                                    prepender = $('<div>' + chat_content + rest_messages + '</div>')
                                } else if (value.you_say === false) {
                                    like_count = value.like_count

                                    var heart;
                                    if (value.you_like === true) {
                                        heart = 'glyphicon-heart'
                                    } else {
                                        heart = 'glyphicon-heart-empty'
                                    }
                                    like = '<a href=""><span class="glyphicon ' + heart + ' reading_like" id="reading_like_span_' + value.id + '" data-u="' + value.id + '"></span></a><span class="reading_like_text"> </span><a href=""><span class="reading_like_text" id="reading_like_count_' + value.id + '">' + like_count + '</span></a>'

                                    if (value.rest_count === 0) {
                                        rest_messages = ''
                                    } else {
                                        rest_messages = '<div id="rest_wrapper_' + value.id + '"><a href=""><div class="reading_chat_rest_messages clickable" id="rest_start_' + value.id + '" data-u="' + value.id + '" align="center">' + value.rest_count + ' messages</div></a></div><a href=""><div id="rest_more_' + value.id + '" class="rest_more_load reading_chat_rest_messages hidden" data-u="' + value.id + '" align="center">more</div></a><div class="hidden" id="rest_last_' + value.id + '"></div>'
                                    }

                                    chat_content = '<div class="reading_chat_content_someone">' +
                                        '<div><img class="reading_chat_img" src="' + value.content + '">' + like + '</div>'
                                    '</div>'
                                    prepender = $('<div>' + chat_content + rest_messages + '</div>')
                                }

                                break;
                            default:
                                break;
                        }

                        prepender.find('#reading_like_count_' + value.id).on('click', function (e) {
                            e.preventDefault()
                            if ($('#user_id').html() === '') {
                                $('#modal_need_login').modal('show')
                                return false;
                            }
                            $('#clicked_post_chat_id').html(value.id)
                            $('#modal_post_chat_liking').modal('show')
                        });

                        prepender.find('.reading_like').on('click', function (e) {

                            e.preventDefault()
                            if ($('#user_id').html() === '') {
                                $('#modal_need_login').modal('show')
                                return false;
                            }
                            var post_chat_id = $(this).attr('data-u')

                            $.ajax({
                                url: '/re/post/chat/like/', type: 'post', dataType: 'json', cache: false,
                                data: {
                                    post_chat_id: post_chat_id,
                                },
                                success: function (data) {
                                    if (data.res === 1) {
                                        var has_k = $('#reading_like_count_' + post_chat_id).html()

                                        if (data.liked === true) {
                                            if (!(has_k.includes('k'))) {
                                                $('#reading_like_count_' + post_chat_id).html(parseInt(has_k) + 1)
                                            }
                                            $('#reading_like_span_' + post_chat_id).removeClass('glyphicon-heart-empty')
                                            $('#reading_like_span_' + post_chat_id).addClass('glyphicon-heart')
                                        } else {
                                            if (!(has_k.includes('k'))) {
                                                $('#reading_like_count_' + post_chat_id).html(parseInt(has_k) - 1)
                                            }
                                            $('#reading_like_span_' + post_chat_id).removeClass('glyphicon-heart')
                                            $('#reading_like_span_' + post_chat_id).addClass('glyphicon-heart-empty')
                                        }
                                    }
                                }
                            })

                        });
                        prepender.find('.reading_chat_rest_messages').on('click', function (e) {
                            e.preventDefault()
                            var post_chat_id = $(this).attr('data-u')
                            $.ajax({
                                url: '/re/post/chat/rest/more/load/', type: 'post', dataType: 'json', cache: false,
                                data: {
                                    last_id: $('#rest_last_' + post_chat_id).html(),
                                    post_chat_id: post_chat_id,
                                },
                                success: function (data) {
                                    if (!($('#rest_start_' + post_chat_id).hasClass('hidden'))) {
                                        $('#rest_start_' + post_chat_id).addClass('hidden')
                                    }

                                    if (data.rest_next === true) {
                                        $('#rest_more_' + post_chat_id).removeClass('hidden')
                                    } else {
                                        $('#rest_more_' + post_chat_id).addClass('hidden')
                                    }

                                    $.each(data.set, function (key, value) {
                                        var like_count = value.like_count

                                        var like = ''
                                        if (value.you_like === true) {
                                            like = 'glyphicon-heart'
                                        } else {
                                            like = 'glyphicon-heart-empty'
                                        }
                                        var delete_div = ''
                                        if (value.user_id === $('#user_id').html() || $('#user_id').html() === $('#reading_post_user_id').html()) {
                                            delete_div = '<div align="right"><a href=""><span class="reading_chat_rest_messages_delete">delete</span></a></div>'
                                        }
                                        var pre_rest_appender = '<div class="reading_chat_rest" align="right" id="reading_chat_rest_wrapper_' + value.id + '">' +
                                            '<div class="reading_chat_content">' +
                                            '<div class="reading_chat_rest_name"><a href="/' + value.username + '/"><span>' + value.name + '[' + value.username + ']' + '</span></a></div>\n' +
                                            '<div class="reading_chat_rest_text">' + value.text + '<span>   </span><span class="reading_chat_rest_time">' + date_differ(value.created) + '</span>' +
                                            '<a href=""><span id="rest_like_span_' + value.id + '" class="glyphicon ' + like + ' reading_like"></span></a><span class="reading_like_text"> </span><a href=""><span class="reading_like_text" id="rest_like_' + value.id + '" data-u="' + value.like_count + '">' + like_count + '</span></a>' +
                                            '</div>' +
                                            '</div>' +
                                            delete_div +
                                            '</div>'
                                        var rest_appender = $(pre_rest_appender)
                                        rest_appender.find('#rest_like_' + value.id).on('click', function (e) {
                                            e.preventDefault()
                                            if ($('#user_id').html() === '') {
                                                $('#modal_need_login').modal('show')
                                                return false;
                                            }

                                            $('#clicked_post_chat_rest_id').html(value.id)
                                            $('#modal_post_chat_rest_liking').modal('show')
                                        })
                                        rest_appender.find('.reading_like').on('click', function (e) {
                                            e.preventDefault()

                                            if ($('#user_id').html() === '') {
                                                $('#modal_need_login').modal('show')
                                                return false;
                                            }
                                            $.ajax({
                                                url: '/re/post/chat/rest/like/',
                                                type: 'post',
                                                dataType: 'json',
                                                cache: false,
                                                data: {
                                                    rest_id: value.id,
                                                },
                                                success: function (data) {
                                                    if (data.res === 1) {
                                                        var has_k = $('#rest_like_' + value.id).html()

                                                        if (data.liked === true) {
                                                            if (!(has_k.includes('k'))) {
                                                                $('#rest_like_' + value.id).html(parseInt(has_k) + 1)
                                                            }
                                                            $('#rest_like_span_' + value.id).removeClass('glyphicon-heart-empty')
                                                            $('#rest_like_span_' + value.id).addClass('glyphicon-heart')
                                                        } else {
                                                            if (!(has_k.includes('k'))) {
                                                                $('#rest_like_' + value.id).html(parseInt(has_k) - 1)
                                                            }
                                                            $('#rest_like_span_' + value.id).removeClass('glyphicon-heart')
                                                            $('#rest_like_span_' + value.id).addClass('glyphicon-heart-empty')
                                                        }
                                                    }
                                                }
                                            })
                                        })
                                        rest_appender.find('.reading_chat_rest_messages_delete').on('click', function (e) {
                                            e.preventDefault()

                                            if ($('#user_id').html() === '') {
                                                $('#modal_need_login').modal('show')
                                                return false;
                                            }
                                            $.ajax({
                                                url: '/re/post/chat/rest/delete/',
                                                type: 'post',
                                                dataType: 'json',
                                                cache: false,
                                                data: {
                                                    rest_id: value.id,
                                                },
                                                success: function (data) {
                                                    if (data.res === 1) {
                                                        if (data.deleted === true) {
                                                            $('#reading_chat_rest_wrapper_' + value.id).replaceWith('<div align="right">removed</div>')
                                                        }
                                                    }
                                                }
                                            })
                                        })

                                        $('#rest_wrapper_' + post_chat_id).append(rest_appender)
                                        $('#rest_last_' + post_chat_id).html(value.id)
                                    })
                                }
                            })


                        })

                        $('#modal_reading_chat').prepend(prepender)

                    })


                    if (data.next === null) {
                        if ($('#reading_post_user_id').html() === $('#user_id').html()) {
                            $('.reading_chat_next').addClass('hidden')
                            $('#interaction_update').removeClass('hidden')
                        } else {
                            $('.reading_chat_next').addClass('hidden')
                            $('#interaction_form').removeClass('hidden')
                        }
                    } else {

                        $('#reading_post_chat_next_id').html(data.next.content.id)
                        if (data.next.content.you_say === true) {
                            $('.reading_chat_next').addClass('hidden')
                            $('#interaction_play_white').removeClass('hidden')
                        } else if (data.next.content.you_say === false) {
                            $('.reading_chat_next').addClass('hidden')
                            $('#interaction_play_green').removeClass('hidden')
                        }

                    }

                    if (start === false) {
                        $('#reading_chat_more_load').removeClass('hidden')
                        $('#reading_chat_started').addClass('hidden')
                    } else {
                        $('#reading_chat_more_load').addClass('hidden')
                        $('#reading_chat_started').removeClass('hidden')
                    }

                    $(".modal_reading_chat").animate({scrollTop: $('.modal_reading_chat').prop("scrollHeight")}, 400);

                }
            }
        })


    }).on("hidden.bs.modal", function () {
        var post_id = $('#reading_post_id').html()

        var appender = '<div class="row div_base" id="post_div_' + post_id + '" data-u="' + post_id + '">' +
            '<script defer>' +
            '    home_populate("' + post_id + '")' +
            '<' + '/script></div>'

        //'console.log($("#post_div_'+value.id+'").attr("data-u"))' +
        $('#post_div_' + post_id).replaceWith(appender)
        $('#modal_reading_chat').empty()
    });
    $('#reading_chat_more_load').click(function (e) {
        e.preventDefault()

        var reading_post_id = $('#reading_post_id').html()
        var reading_post_profile_photo = $('#reading_post_profile_photo').html()
        var reading_post_profile_name = $('#reading_post_profile_name').html()
        $.ajax({
            url: '/re/post/reading/more/load/', type: 'post', dataType: 'json', cache: false,
            data: {
                post_chat_before_id: $('#reading_post_chat_before_id').html(),
                post_id: $('#reading_post_id').html()
            },
            success: function (data) {
//------------------------------------------------------------------------------
                //-------------------------------------------------------------------------

                if (data.res === 1) {
                    var start = false
                    $.each(data.set, function (key, value) {
                        var prepender;
                        $('#reading_post_chat_before_id').html(value.id)

                        var align, profile_photo, chat_content, like, like_count, rest_messages;
                        switch (value.kind) {
                            case 'start':
                                start = true
                                if (value.rest_count === 0) {
                                    rest_messages = ''
                                } else if (value.rest_count < 1000) {
                                    rest_messages = '<div id="rest_wrapper_' + value.id + '"><a href=""><div class="reading_chat_rest_messages clickable" id="rest_start_' + value.id + '" data-u="' + value.id + '" align="center">' + value.rest_count + ' messages</div></a></div><a href=""><div id="rest_more_' + value.id + '" class="rest_more_load reading_chat_rest_messages hidden" data-u="' + value.id + '" align="center">more</div></a><div class="hidden" id="rest_last_' + value.id + '"></div>'
                                } else if (1000 <= value.rest_count) {
                                    rest_messages = '<div id="rest_wrapper_' + value.id + '"><a href=""><div class="reading_chat_rest_messages clickable" id="rest_start_' + value.id + '" data-u="' + value.id + '" align="center">' + parseInt(value.like_count / 1000) + 'k' + ' messages</div></a></div><a href=""><div id="rest_more_' + value.id + '" class="rest_more_load reading_chat_rest_messages hidden" data-u="' + value.id + '" align="center">more</div></a><div class="hidden" id="rest_last_' + value.id + '"></div>'
                                }
                                prepender = $(rest_messages)
                                break;
                            case 'text':
                                if (value.you_say === true) {
                                    like_count = value.like_count

                                    var heart;
                                    if (value.you_like === true) {
                                        heart = 'glyphicon-heart'
                                    } else {
                                        heart = 'glyphicon-heart-empty'
                                    }
                                    like = '<a href=""><span class="glyphicon ' + heart + ' reading_like" id="reading_like_span_' + value.id + '" data-u="' + value.id + '"></span></a><span class="reading_like_text"> </span><a href=""><span class="reading_like_text" id="reading_like_count_' + value.id + '">' + like_count + '</span></a>'

                                    chat_content = '<div class="reading_chat_content_i">' +
                                        '<div>' + value.content + like + '</div>' +
                                        '</div>'

                                    if (value.rest_count === 0) {
                                        rest_messages = ''
                                    } else {
                                        rest_messages = '<div id="rest_wrapper_' + value.id + '"><a href=""><div class="reading_chat_rest_messages clickable" id="rest_start_' + value.id + '" data-u="' + value.id + '" align="center">' + value.rest_count + ' messages</div></a></div><a href=""><div id="rest_more_' + value.id + '" class="rest_more_load reading_chat_rest_messages hidden" data-u="' + value.id + '" align="center">more</div></a><div class="hidden" id="rest_last_' + value.id + '"></div>'
                                    }

                                    prepender = $('<div>' + chat_content + rest_messages + '</div>')

                                } else if (value.you_say === false) {
                                    like_count = value.like_count

                                    var heart;
                                    if (value.you_like === true) {
                                        heart = 'glyphicon-heart'
                                    } else {
                                        heart = 'glyphicon-heart-empty'
                                    }
                                    like = '<a href=""><span class="glyphicon ' + heart + ' reading_like" id="reading_like_span_' + value.id + '" data-u="' + value.id + '"></span></a><span class="reading_like_text"> </span><a href=""><span class="reading_like_text" id="reading_like_count_' + value.id + '">' + like_count + '</span></a>'

                                    chat_content = '<div class="reading_chat_content_someone">' +
                                        '<div>' + value.content + like + '</div>' +
                                        '</div>'

                                    if (value.rest_count === 0) {
                                        rest_messages = ''
                                    } else {
                                        rest_messages = '<div id="rest_wrapper_' + value.id + '"><a href=""><div class="reading_chat_rest_messages clickable" id="rest_start_' + value.id + '" data-u="' + value.id + '" align="center">' + value.rest_count + ' messages</div></a></div><a href=""><div id="rest_more_' + value.id + '" class="rest_more_load reading_chat_rest_messages hidden" data-u="' + value.id + '" align="center">more</div></a><div class="hidden" id="rest_last_' + value.id + '"></div>'
                                    }

                                    prepender = $('<div>' + chat_content + rest_messages + '</div>')


                                }

                                break;

                            case 'photo':

                                if (value.you_say === true) {

                                    like_count = value.like_count

                                    var heart;
                                    if (value.you_like === true) {
                                        heart = 'glyphicon-heart'
                                    } else {
                                        heart = 'glyphicon-heart-empty'
                                    }
                                    like = '<a href=""><span class="glyphicon ' + heart + ' reading_like" id="reading_like_span_' + value.id + '" data-u="' + value.id + '"></span></a><span class="reading_like_text"> </span><a href=""><span class="reading_like_text" id="reading_like_count_' + value.id + '">' + like_count + '</span></a>'

                                    if (value.rest_count === 0) {
                                        rest_messages = ''
                                    } else {
                                        rest_messages = '<div id="rest_wrapper_' + value.id + '"><a href=""><div class="reading_chat_rest_messages clickable" id="rest_start_' + value.id + '" data-u="' + value.id + '" align="center">' + value.rest_count + ' messages</div></a></div><a href=""><div id="rest_more_' + value.id + '" class="rest_more_load reading_chat_rest_messages hidden" data-u="' + value.id + '" align="center">more</div></a><div class="hidden" id="rest_last_' + value.id + '"></div>'
                                    }

                                    chat_content = '<div class="reading_chat_content_i">' +
                                        '<div><img class="reading_chat_img" src="' + value.content + '">' + like + '</div>' +
                                        '</div>'
                                    prepender = $('<div>' + chat_content + rest_messages + '</div>')
                                } else if (value.you_say === false) {
                                    like_count = value.like_count

                                    var heart;
                                    if (value.you_like === true) {
                                        heart = 'glyphicon-heart'
                                    } else {
                                        heart = 'glyphicon-heart-empty'
                                    }
                                    like = '<a href=""><span class="glyphicon ' + heart + ' reading_like" id="reading_like_span_' + value.id + '" data-u="' + value.id + '"></span></a><span class="reading_like_text"> </span><a href=""><span class="reading_like_text" id="reading_like_count_' + value.id + '">' + like_count + '</span></a>'

                                    if (value.rest_count === 0) {
                                        rest_messages = ''
                                    } else {
                                        rest_messages = '<div id="rest_wrapper_' + value.id + '"><a href=""><div class="reading_chat_rest_messages clickable" id="rest_start_' + value.id + '" data-u="' + value.id + '" align="center">' + value.rest_count + ' messages</div></a></div><a href=""><div id="rest_more_' + value.id + '" class="rest_more_load reading_chat_rest_messages hidden" data-u="' + value.id + '" align="center">more</div></a><div class="hidden" id="rest_last_' + value.id + '"></div>'
                                    }

                                    chat_content = '<div class="reading_chat_content_someone">' +
                                        '<div><img class="reading_chat_img" src="' + value.content + '">' + like + '</div>'
                                    '</div>'
                                    prepender = $('<div>' + chat_content + rest_messages + '</div>')
                                }

                                break;
                            default:
                                break;
                        }

                        prepender.find('#reading_like_count_' + value.id).on('click', function (e) {
                            e.preventDefault()
                            if ($('#user_id').html() === '') {
                                $('#modal_need_login').modal('show')
                                return false;
                            }
                            $('#clicked_post_chat_id').html(value.id)
                            $('#modal_post_chat_liking').modal('show')
                        });
                        prepender.find('.reading_like').on('click', function (e) {

                            e.preventDefault()
                            if ($('#user_id').html() === '') {
                                $('#modal_need_login').modal('show')
                                return false;
                            }
                            var post_chat_id = $(this).attr('data-u')

                            $.ajax({
                                url: '/re/post/chat/like/', type: 'post', dataType: 'json', cache: false,
                                data: {
                                    post_chat_id: post_chat_id,
                                },
                                success: function (data) {
                                    if (data.res === 1) {
                                        var has_k = $('#reading_like_count_' + post_chat_id).html()

                                        if (data.liked === true) {
                                            if (!(has_k.includes('k'))) {
                                                $('#reading_like_count_' + post_chat_id).html(parseInt(has_k) + 1)
                                            }
                                            $('#reading_like_span_' + post_chat_id).removeClass('glyphicon-heart-empty')
                                            $('#reading_like_span_' + post_chat_id).addClass('glyphicon-heart')
                                        } else {
                                            if (!(has_k.includes('k'))) {
                                                $('#reading_like_count_' + post_chat_id).html(parseInt(has_k) - 1)
                                            }
                                            $('#reading_like_span_' + post_chat_id).removeClass('glyphicon-heart')
                                            $('#reading_like_span_' + post_chat_id).addClass('glyphicon-heart-empty')
                                        }
                                    }
                                }
                            })

                        });
                        prepender.find('.reading_chat_rest_messages').on('click', function (e) {
                            e.preventDefault()
                            var post_chat_id = $(this).attr('data-u')
                            $.ajax({
                                url: '/re/post/chat/rest/more/load/', type: 'post', dataType: 'json', cache: false,
                                data: {
                                    last_id: $('#rest_last_' + post_chat_id).html(),
                                    post_chat_id: post_chat_id,
                                },
                                success: function (data) {
                                    if (!($('#rest_start_' + post_chat_id).hasClass('hidden'))) {
                                        $('#rest_start_' + post_chat_id).addClass('hidden')
                                    }

                                    if (data.rest_next === true) {
                                        $('#rest_more_' + post_chat_id).removeClass('hidden')
                                    } else {
                                        $('#rest_more_' + post_chat_id).addClass('hidden')
                                    }

                                    $.each(data.set, function (key, value) {
                                        var like_count = value.like_count

                                        var like = ''
                                        if (value.you_like === true) {
                                            like = 'glyphicon-heart'
                                        } else {
                                            like = 'glyphicon-heart-empty'
                                        }
                                        var delete_div = ''
                                        if (value.user_id === $('#user_id').html() || $('#user_id').html() === $('#reading_post_user_id').html()) {
                                            delete_div = '<div align="right"><a href=""><span class="reading_chat_rest_messages_delete">delete</span></a></div>'
                                        }
                                        var pre_rest_appender = '<div class="reading_chat_rest" align="right" id="reading_chat_rest_wrapper_' + value.id + '">' +
                                            '<div class="reading_chat_content">' +
                                            '<div class="reading_chat_rest_name"><a href="/' + value.username + '/"><span>' + value.name + '[' + value.username + ']' + '</span></a></div>\n' +
                                            '<div class="reading_chat_rest_text">' + value.text + '<span>   </span><span class="reading_chat_rest_time">' + date_differ(value.created) + '</span>' +
                                            '<a href=""><span id="rest_like_span_' + value.id + '" class="glyphicon ' + like + ' reading_like"></span></a><span class="reading_like_text"> </span><a href=""><span class="reading_like_text" id="rest_like_' + value.id + '" data-u="' + value.like_count + '">' + like_count + '</span></a>' +
                                            '</div>' +
                                            '</div>' +
                                            delete_div +
                                            '</div>'
                                        var rest_appender = $(pre_rest_appender)

                                        rest_appender.find('#rest_like_' + value.id).on('click', function (e) {
                                            e.preventDefault()
                                            if ($('#user_id').html() === '') {
                                                $('#modal_need_login').modal('show')
                                                return false;
                                            }
                                            $('#clicked_post_chat_rest_id').html(value.id)
                                            $('#modal_post_chat_rest_liking').modal('show')
                                        })
                                        rest_appender.find('.reading_like').on('click', function (e) {
                                            e.preventDefault()
                                            if ($('#user_id').html() === '') {
                                                $('#modal_need_login').modal('show')
                                                return false;
                                            }
                                            $.ajax({
                                                url: '/re/post/chat/rest/like/',
                                                type: 'post',
                                                dataType: 'json',
                                                cache: false,
                                                data: {
                                                    rest_id: value.id,
                                                },
                                                success: function (data) {
                                                    if (data.res === 1) {
                                                        var has_k = $('#rest_like_' + value.id).html()

                                                        if (data.liked === true) {
                                                            if (!(has_k.includes('k'))) {
                                                                $('#rest_like_' + value.id).html(parseInt(has_k) + 1)
                                                            }
                                                            $('#rest_like_span_' + value.id).removeClass('glyphicon-heart-empty')
                                                            $('#rest_like_span_' + value.id).addClass('glyphicon-heart')
                                                        } else {
                                                            if (!(has_k.includes('k'))) {
                                                                $('#rest_like_' + value.id).html(parseInt(has_k) - 1)
                                                            }
                                                            $('#rest_like_span_' + value.id).removeClass('glyphicon-heart')
                                                            $('#rest_like_span_' + value.id).addClass('glyphicon-heart-empty')
                                                        }
                                                    }
                                                }
                                            })
                                        })
                                        rest_appender.find('.reading_chat_rest_messages_delete').on('click', function (e) {
                                            e.preventDefault()

                                            if ($('#user_id').html() === '') {
                                                $('#modal_need_login').modal('show')
                                                return false;
                                            }
                                            $.ajax({
                                                url: '/re/post/chat/rest/delete/',
                                                type: 'post',
                                                dataType: 'json',
                                                cache: false,
                                                data: {
                                                    rest_id: value.id,
                                                },
                                                success: function (data) {
                                                    if (data.res === 1) {
                                                        if (data.deleted === true) {
                                                            $('#reading_chat_rest_wrapper_' + value.id).replaceWith('<div align="right">removed</div>')
                                                        }
                                                    }
                                                }
                                            })
                                        })

                                        $('#rest_wrapper_' + post_chat_id).append(rest_appender)
                                        $('#rest_last_' + post_chat_id).html(value.id)
                                    })
                                }
                            })


                        })

                        $('#modal_reading_chat').prepend(prepender)

                    })


                    if (start === false) {
                        $('#reading_chat_more_load').removeClass('hidden')
                        $('#reading_chat_started').addClass('hidden')
                    } else {
                        $('#reading_chat_more_load').addClass('hidden')
                        $('#reading_chat_started').removeClass('hidden')
                    }
                }

            }
        })
    })
    $('#interaction_choice_interact').click(function (e) {
        e.preventDefault()
        $('.reading_chat_next').addClass('hidden')
        $('#you_say_form').removeClass('hidden')
    })
    $('#interaction_choice_update').click(function (e) {
        e.preventDefault()
        var scheme = window.location.protocol == "https:" ? "https" : "http";
        var path = scheme + '://' + window.location.host + "/post/update/";
        location.href = path + $('#reading_post_id').html()
    })
    $('.reading_chat_play').click(function (e) {
        e.preventDefault()


        var reading_post_id = $('#reading_post_id').html()
        var reading_post_profile_photo = $('#reading_post_profile_photo').html()
        var reading_post_profile_name = $('#reading_post_profile_name').html()
        $.ajax({
            url: '/re/post/chat/next/load/', type: 'post', dataType: 'json', cache: false,
            data: {
                post_chat_next_id: $('#reading_post_chat_next_id').html(),
            },
            success: function (data) {
                var prepender, align, profile_photo, chat_content, like, like_count, rest_messages;
                var start = false
                var last_id;
                $.each(data.set, function (key, value) {
                    $('#reading_post_chat_last_id').html(value.id)
                    switch (value.kind) {
                        case 'start':
                            start = true
                            if (value.rest_count === 0) {
                                rest_messages = ''
                            } else if (value.rest_count < 1000) {
                                rest_messages = '<div id="rest_wrapper_' + value.id + '"><a href=""><div class="reading_chat_rest_messages clickable" id="rest_start_' + value.id + '" data-u="' + value.id + '" align="center">' + value.rest_count + ' messages</div></a></div><a href=""><div id="rest_more_' + value.id + '" class="rest_more_load reading_chat_rest_messages hidden" data-u="' + value.id + '" align="center">more</div></a><div class="hidden" id="rest_last_' + value.id + '"></div>'
                            } else if (1000 <= value.rest_count) {
                                rest_messages = '<div id="rest_wrapper_' + value.id + '"><a href=""><div class="reading_chat_rest_messages clickable" id="rest_start_' + value.id + '" data-u="' + value.id + '" align="center">' + parseInt(value.like_count / 1000) + 'k' + ' messages</div></a></div><a href=""><div id="rest_more_' + value.id + '" class="rest_more_load reading_chat_rest_messages hidden" data-u="' + value.id + '" align="center">more</div></a><div class="hidden" id="rest_last_' + value.id + '"></div>'
                            }
                            prepender = $(rest_messages)
                            break;
                        case 'text':
                            if (value.you_say === true) {
                                like_count = value.like_count

                                var heart;
                                if (value.you_like === true) {
                                    heart = 'glyphicon-heart'
                                } else {
                                    heart = 'glyphicon-heart-empty'
                                }
                                like = '<a href=""><span class="glyphicon ' + heart + ' reading_like" id="reading_like_span_' + value.id + '" data-u="' + value.id + '"></span></a><span class="reading_like_text"> </span><a href=""><span class="reading_like_text" id="reading_like_count_' + value.id + '">' + like_count + '</span></a>'

                                chat_content = '<div class="reading_chat_content_i">' +
                                    '<div>' + value.content + like + '</div>' +
                                    '</div>'

                                if (value.rest_count === 0) {
                                    rest_messages = ''
                                } else {
                                    rest_messages = '<div id="rest_wrapper_' + value.id + '"><a href=""><div class="reading_chat_rest_messages clickable" id="rest_start_' + value.id + '" data-u="' + value.id + '" align="center">' + value.rest_count + ' messages</div></a></div><a href=""><div id="rest_more_' + value.id + '" class="rest_more_load reading_chat_rest_messages hidden" data-u="' + value.id + '" align="center">more</div></a><div class="hidden" id="rest_last_' + value.id + '"></div>'
                                }

                                prepender = $('<div>' + chat_content + rest_messages + '</div>')

                            } else if (value.you_say === false) {
                                like_count = value.like_count

                                var heart;
                                if (value.you_like === true) {
                                    heart = 'glyphicon-heart'
                                } else {
                                    heart = 'glyphicon-heart-empty'
                                }
                                like = '<a href=""><span class="glyphicon ' + heart + ' reading_like" id="reading_like_span_' + value.id + '" data-u="' + value.id + '"></span></a><span class="reading_like_text"> </span><a href=""><span class="reading_like_text" id="reading_like_count_' + value.id + '">' + like_count + '</span></a>'

                                chat_content = '<div class="reading_chat_content_someone">' +
                                    '<div>' + value.content + like + '</div>' +
                                    '</div>'

                                if (value.rest_count === 0) {
                                    rest_messages = ''
                                } else {
                                    rest_messages = '<div id="rest_wrapper_' + value.id + '"><a href=""><div class="reading_chat_rest_messages clickable" id="rest_start_' + value.id + '" data-u="' + value.id + '" align="center">' + value.rest_count + ' messages</div></a></div><a href=""><div id="rest_more_' + value.id + '" class="rest_more_load reading_chat_rest_messages hidden" data-u="' + value.id + '" align="center">more</div></a><div class="hidden" id="rest_last_' + value.id + '"></div>'
                                }

                                prepender = $('<div>' + chat_content + rest_messages + '</div>')


                            }

                            break;

                        case 'photo':

                            if (value.you_say === true) {

                                like_count = value.like_count

                                var heart;
                                if (value.you_like === true) {
                                    heart = 'glyphicon-heart'
                                } else {
                                    heart = 'glyphicon-heart-empty'
                                }
                                like = '<a href=""><span class="glyphicon ' + heart + ' reading_like" id="reading_like_span_' + value.id + '" data-u="' + value.id + '"></span></a><span class="reading_like_text"> </span><a href=""><span class="reading_like_text" id="reading_like_count_' + value.id + '">' + like_count + '</span></a>'

                                if (value.rest_count === 0) {
                                    rest_messages = ''
                                } else {
                                    rest_messages = '<div id="rest_wrapper_' + value.id + '"><a href=""><div class="reading_chat_rest_messages clickable" id="rest_start_' + value.id + '" data-u="' + value.id + '" align="center">' + value.rest_count + ' messages</div></a></div><a href=""><div id="rest_more_' + value.id + '" class="rest_more_load reading_chat_rest_messages hidden" data-u="' + value.id + '" align="center">more</div></a><div class="hidden" id="rest_last_' + value.id + '"></div>'
                                }

                                chat_content = '<div class="reading_chat_content_i">' +
                                    '<div><img class="reading_chat_img" src="' + value.content + '">' + like + '</div>' +
                                    '</div>'
                                prepender = $('<div>' + chat_content + rest_messages + '</div>')
                            } else if (value.you_say === false) {
                                like_count = value.like_count

                                var heart;
                                if (value.you_like === true) {
                                    heart = 'glyphicon-heart'
                                } else {
                                    heart = 'glyphicon-heart-empty'
                                }
                                like = '<a href=""><span class="glyphicon ' + heart + ' reading_like" id="reading_like_span_' + value.id + '" data-u="' + value.id + '"></span></a><span class="reading_like_text"> </span><a href=""><span class="reading_like_text" id="reading_like_count_' + value.id + '">' + like_count + '</span></a>'

                                if (value.rest_count === 0) {
                                    rest_messages = ''
                                } else {
                                    rest_messages = '<div id="rest_wrapper_' + value.id + '"><a href=""><div class="reading_chat_rest_messages clickable" id="rest_start_' + value.id + '" data-u="' + value.id + '" align="center">' + value.rest_count + ' messages</div></a></div><a href=""><div id="rest_more_' + value.id + '" class="rest_more_load reading_chat_rest_messages hidden" data-u="' + value.id + '" align="center">more</div></a><div class="hidden" id="rest_last_' + value.id + '"></div>'
                                }

                                chat_content = '<div class="reading_chat_content_someone">' +
                                    '<div><img class="reading_chat_img" src="' + value.content + '">' + like + '</div>'
                                '</div>'
                                prepender = $('<div>' + chat_content + rest_messages + '</div>')
                            }

                            break;
                        default:
                            break;
                    }
                    prepender.find('#reading_like_count_' + value.id).on('click', function (e) {
                        e.preventDefault()
                        if ($('#user_id').html() === '') {
                            $('#modal_need_login').modal('show')
                            return false;
                        }
                        $('#clicked_post_chat_id').html(value.id)
                        $('#modal_post_chat_liking').modal('show')
                    });

                    prepender.find('.reading_like').on('click', function (e) {

                        e.preventDefault()
                        if ($('#user_id').html() === '') {
                            $('#modal_need_login').modal('show')
                            return false;
                        }
                        var post_chat_id = $(this).attr('data-u')

                        $.ajax({
                            url: '/re/post/chat/like/', type: 'post', dataType: 'json', cache: false,
                            data: {
                                post_chat_id: post_chat_id,
                            },
                            success: function (data) {
                                if (data.res === 1) {
                                    var has_k = $('#reading_like_count_' + post_chat_id).html()

                                    if (data.liked === true) {
                                        if (!(has_k.includes('k'))) {
                                            $('#reading_like_count_' + post_chat_id).html(parseInt(has_k) + 1)
                                        }
                                        $('#reading_like_span_' + post_chat_id).removeClass('glyphicon-heart-empty')
                                        $('#reading_like_span_' + post_chat_id).addClass('glyphicon-heart')
                                    } else {
                                        if (!(has_k.includes('k'))) {
                                            $('#reading_like_count_' + post_chat_id).html(parseInt(has_k) - 1)
                                        }
                                        $('#reading_like_span_' + post_chat_id).removeClass('glyphicon-heart')
                                        $('#reading_like_span_' + post_chat_id).addClass('glyphicon-heart-empty')
                                    }
                                }
                            }
                        })

                    });

                    prepender.find('.reading_chat_rest_messages').on('click', function (e) {
                        e.preventDefault()
                        var post_chat_id = $(this).attr('data-u')
                        $.ajax({
                            url: '/re/post/chat/rest/more/load/', type: 'post', dataType: 'json', cache: false,
                            data: {
                                last_id: $('#rest_last_' + post_chat_id).html(),
                                post_chat_id: post_chat_id,
                            },
                            success: function (data) {
                                if (!($('#rest_start_' + post_chat_id).hasClass('hidden'))) {
                                    $('#rest_start_' + post_chat_id).addClass('hidden')
                                }

                                if (data.rest_next === true) {
                                    $('#rest_more_' + post_chat_id).removeClass('hidden')
                                } else {
                                    $('#rest_more_' + post_chat_id).addClass('hidden')
                                }

                                $.each(data.set, function (key, value) {
                                    var like_count = value.like_count

                                    var like = ''
                                    if (value.you_like === true) {
                                        like = 'glyphicon-heart'
                                    } else {
                                        like = 'glyphicon-heart-empty'
                                    }
                                    var delete_div = ''
                                    if (value.user_id === $('#user_id').html() || $('#user_id').html() === $('#reading_post_user_id').html()) {
                                        delete_div = '<div align="right"><a href=""><span class="reading_chat_rest_messages_delete">delete</span></a></div>'
                                    }
                                    var pre_rest_appender = '<div class="reading_chat_rest" align="right" id="reading_chat_rest_wrapper_' + value.id + '">' +
                                        '<div class="reading_chat_content">' +
                                        '<div class="reading_chat_rest_name"><a href="/' + value.username + '/"><span>' + value.name + '[' + value.username + ']' + '</span></a></div>\n' +
                                        '<div class="reading_chat_rest_text">' + value.text + '<span>   </span><span class="reading_chat_rest_time">' + date_differ(value.created) + '</span>' +
                                        '<a href=""><span id="rest_like_span_' + value.id + '" class="glyphicon ' + like + ' reading_like"></span></a><span class="reading_like_text"> </span><a href=""><span class="reading_like_text" id="rest_like_' + value.id + '" data-u="' + value.like_count + '">' + like_count + '</span></a>' +
                                        '</div>' +
                                        '</div>' +
                                        delete_div +
                                        '</div>'
                                    var rest_appender = $(pre_rest_appender)

                                    rest_appender.find('#rest_like_' + value.id).on('click', function (e) {
                                        e.preventDefault()
                                        if ($('#user_id').html() === '') {
                                            $('#modal_need_login').modal('show')
                                            return false;
                                        }
                                        $('#clicked_post_chat_rest_id').html(value.id)
                                        $('#modal_post_chat_rest_liking').modal('show')
                                    })
                                    rest_appender.find('.reading_like').on('click', function (e) {
                                        e.preventDefault()
                                        if ($('#user_id').html() === '') {
                                            $('#modal_need_login').modal('show')
                                            return false;
                                        }
                                        $.ajax({
                                            url: '/re/post/chat/rest/like/',
                                            type: 'post',
                                            dataType: 'json',
                                            cache: false,
                                            data: {
                                                rest_id: value.id,
                                            },
                                            success: function (data) {
                                                if (data.res === 1) {
                                                    var has_k = $('#rest_like_' + value.id).html()

                                                    if (data.liked === true) {
                                                        if (!(has_k.includes('k'))) {
                                                            $('#rest_like_' + value.id).html(parseInt(has_k) + 1)
                                                        }
                                                        $('#rest_like_span_' + value.id).removeClass('glyphicon-heart-empty')
                                                        $('#rest_like_span_' + value.id).addClass('glyphicon-heart')
                                                    } else {
                                                        if (!(has_k.includes('k'))) {
                                                            $('#rest_like_' + value.id).html(parseInt(has_k) - 1)
                                                        }
                                                        $('#rest_like_span_' + value.id).removeClass('glyphicon-heart')
                                                        $('#rest_like_span_' + value.id).addClass('glyphicon-heart-empty')
                                                    }
                                                }
                                            }
                                        })
                                    })
                                    rest_appender.find('.reading_chat_rest_messages_delete').on('click', function (e) {
                                        e.preventDefault()
                                        if ($('#user_id').html() === '') {
                                            $('#modal_need_login').modal('show')
                                            return false;
                                        }
                                        $.ajax({
                                            url: '/re/post/chat/rest/delete/',
                                            type: 'post',
                                            dataType: 'json',
                                            cache: false,
                                            data: {
                                                rest_id: value.id,
                                            },
                                            success: function (data) {
                                                if (data.res === 1) {
                                                    if (data.deleted === true) {
                                                        $('#reading_chat_rest_wrapper_' + value.id).replaceWith('<div align="right">removed</div>')
                                                    }
                                                }
                                            }
                                        })
                                    })

                                    $('#rest_wrapper_' + post_chat_id).append(rest_appender)
                                    $('#rest_last_' + post_chat_id).html(value.id)
                                })
                            }
                        })


                    })
                    $('#modal_reading_chat').append(prepender)

                })
                if (data.next === null) {
                    if ($('#reading_post_user_id').html() === $('#user_id').html()) {

                        $('.reading_chat_next').addClass('hidden')
                        $('#interaction_update').removeClass('hidden')
                    } else {
                        $('.reading_chat_next').addClass('hidden')
                        $('#interaction_form').removeClass('hidden')
                    }
                } else {
                    $('#reading_post_chat_next_id').html(data.next.content.id)
                    if (data.next.content.you_say === true) {
                        $('.reading_chat_next').addClass('hidden')
                        $('#interaction_play_white').removeClass('hidden')
                    } else if (data.next.content.you_say === false) {
                        $('.reading_chat_next').addClass('hidden')
                        $('#interaction_play_green').removeClass('hidden')
                    }
                    //다른사람 글 볼때 딜리트 활성화 제거 .
                }

            }
        })
        $(".modal_reading_chat").animate({scrollTop: $('.modal_reading_chat').prop("scrollHeight")}, 500);


    })

    $('#interaction_form_textarea').on("keypress", function (e) {
        if ($('#user_id').html() === '') {
            $('#modal_need_login').modal('show')
            return false;
        }
        /* ENTER PRESSED*/
        if (e.keyCode == 13 && !e.shiftKey) {
            var text = $('#interaction_form_textarea').val()
            if (text === '') {
                return false;
            }
            $.ajax({
                url: '/re/post/chat/add/rest/', type: 'post', dataType: 'json', cache: false,
                data: {
                    post_chat_id: $('#reading_post_chat_last_id').html(),
                    text: text,
                },
                success: function (data) {

                    var delete_div;
                    if (data.set.user_id === $('#user_id').html() || data.set.user_id === $('#reading_post_user_id').html()) {
                        delete_div = '<div align="right"><a href=""><span class="reading_chat_rest_messages_delete">delete</span></a></div>'
                    }
                    var pre_rest_appender = '<div class="reading_chat_rest" align="right" id="reading_chat_rest_wrapper_' + data.set.id + '">' +
                        '<div class="reading_chat_content">' +
                        '<div class="reading_chat_rest_name">' + data.set.name + '</div>\n' +
                        '<div class="reading_chat_rest_text">' + data.set.text +
                        '<a href=""><span id="rest_like_span_' + data.set.id + '"class="glyphicon glyphicon-heart-empty reading_like"></span></a>' +
                        '</div>' +
                        '</div>' +
                        delete_div +
                        '</div>'
                    var rest_appender = $(pre_rest_appender)

                    rest_appender.find('.reading_like').on('click', function (e) {
                        e.preventDefault()
                        $.ajax({
                            url: '/re/post/chat/rest/like/', type: 'post', dataType: 'json', cache: false,
                            data: {
                                rest_id: data.set.id,
                            },
                            success: function (sub_data) {
                                if (sub_data.res === 1) {


                                    if (sub_data.liked === true) {

                                        $('#rest_like_span_' + data.set.id).removeClass('glyphicon-heart-empty')
                                        $('#rest_like_span_' + data.set.id).addClass('glyphicon-heart')
                                    } else {

                                        $('#rest_like_span_' + data.set.id).removeClass('glyphicon-heart')
                                        $('#rest_like_span_' + data.set.id).addClass('glyphicon-heart-empty')
                                    }
                                }
                            }
                        })
                    })
                    rest_appender.find('.reading_chat_rest_messages_delete').on('click', function (e) {
                        e.preventDefault()
                        $.ajax({
                            url: '/re/post/chat/rest/delete/', type: 'post', dataType: 'json', cache: false,
                            data: {
                                rest_id: data.set.id,
                            },
                            success: function (sub_data) {
                                if (sub_data.res === 1) {
                                    if (sub_data.deleted === true) {
                                        $('#reading_chat_rest_wrapper_' + data.set.id).replaceWith('<div align="right">removed</div>')
                                    }
                                }
                            }
                        })
                    })

                    $('#modal_reading_chat').append(rest_appender)
                    $(".modal_reading_chat").animate({scrollTop: $('.modal_reading_chat').prop("scrollHeight")}, 500);

                    $('#interaction_form_textarea').val('')
                }
            })
            return false;

        }

    })

    $('#interaction_form_btn').click(function (e) {
        e.preventDefault()
        if ($('#user_id').html() === '') {
            $('#modal_need_login').modal('show')
            return false;
        }

        var text = $('#interaction_form_textarea').val()
        if (text === '') {
            return false;
        }
        $.ajax({
            url: '/re/post/chat/add/rest/', type: 'post', dataType: 'json', cache: false,
            data: {
                post_chat_id: $('#reading_post_chat_last_id').html(),
                text: text,
            },
            success: function (data) {

                var delete_div;
                if (data.set.user_id === $('#user_id').html() || data.set.user_id === $('#reading_post_user_id').html()) {
                    delete_div = '<div align="right"><a href=""><span class="reading_chat_rest_messages_delete">delete</span></a></div>'
                }
                var pre_rest_appender = '<div class="reading_chat_rest" align="right" id="reading_chat_rest_wrapper_' + data.set.id + '">' +
                    '<div class="reading_chat_content">' +
                    '<div class="reading_chat_rest_name">' + data.set.name + '</div>\n' +
                    '<div class="reading_chat_rest_text">' + data.set.text +
                    '<a href=""><span id="rest_like_span_' + data.set.id + '"class="glyphicon glyphicon-heart-empty reading_like"></span></a>' +
                    '</div>' +
                    '</div>' +
                    delete_div +
                    '</div>'
                var rest_appender = $(pre_rest_appender)

                rest_appender.find('.reading_like').on('click', function (e) {
                    e.preventDefault()
                    $.ajax({
                        url: '/re/post/chat/rest/like/', type: 'post', dataType: 'json', cache: false,
                        data: {
                            rest_id: data.set.id,
                        },
                        success: function (sub_data) {
                            if (sub_data.res === 1) {


                                if (sub_data.liked === true) {

                                    $('#rest_like_span_' + data.set.id).removeClass('glyphicon-heart-empty')
                                    $('#rest_like_span_' + data.set.id).addClass('glyphicon-heart')
                                } else {

                                    $('#rest_like_span_' + data.set.id).removeClass('glyphicon-heart')
                                    $('#rest_like_span_' + data.set.id).addClass('glyphicon-heart-empty')
                                }
                            }
                        }
                    })
                })
                rest_appender.find('.reading_chat_rest_messages_delete').on('click', function (e) {
                    e.preventDefault()
                    $.ajax({
                        url: '/re/post/chat/rest/delete/', type: 'post', dataType: 'json', cache: false,
                        data: {
                            rest_id: data.set.id,
                        },
                        success: function (sub_data) {
                            if (sub_data.res === 1) {
                                if (sub_data.deleted === true) {
                                    $('#reading_chat_rest_wrapper_' + data.set.id).replaceWith('<div align="right">removed</div>')
                                }
                            }
                        }
                    })
                })

                $('#modal_reading_chat').append(rest_appender)
                $(".modal_reading_chat").animate({scrollTop: $('.modal_reading_chat').prop("scrollHeight")}, 500);

                $('#interaction_form_textarea').val('')
            }
        })
        return false;
    })


    $('#you_say_form_textarea').on("keypress", function (e) {
        if ($('#user_id').html() === '') {
            $('#modal_need_login').modal('show')
            return false;
        }
        /* ENTER PRESSED*/
        if (e.keyCode == 13 && !e.shiftKey) {
            var reading_post_id = $('#reading_post_id').html()
            var reading_post_profile_photo = $('#reading_post_profile_photo').html()
            var reading_post_profile_name = $('#reading_post_profile_name').html()

            var text = $('#you_say_form_textarea').val()
            if (text.trim() === '') {
                return false;
            }
            $.ajax({
                url: '/re/post/chat/add/say/', type: 'post', dataType: 'json', cache: false,
                data: {
                    post_id: reading_post_id,
                    post_chat_id: $('#reading_post_chat_last_id').html(),
                    text: text,
                },
                success: function (data) {
                    if (data.res === 1) {
                        var prepender, align, profile_photo, chat_content, like, like_count, rest_messages;
                        $('#reading_post_chat_last_id').html(data.post_chat_id)


                        like_count = 0

                        var heart;
                        heart = 'glyphicon-heart-empty'

                        rest_messages = ''

                        like = '<a href=""><span class="glyphicon ' + heart + ' reading_like" id="reading_like_span_' + data.post_chat_id + '" data-u="' + data.post_chat_id + '"></span></a><span class="reading_like_text"> </span><a href=""><span class="reading_like_text" id="reading_like_count_' + data.post_chat_id + '">' + like_count + '</span></a>'

                        chat_content = '<div class="reading_chat_content_i">' +
                            '<div>' + data.text + like + '</div>' +
                            '</div>'

                        prepender = $('<div>' + chat_content + rest_messages + '</div>')
                        var last_id;

                        prepender.find('#reading_like_count_' + data.post_chat_id).on('click', function (e) {
                            e.preventDefault()
                            if ($('#user_id').html() === '') {
                                $('#modal_need_login').modal('show')
                                return false;
                            }
                            $('#clicked_post_chat_id').html(data.post_chat_id)
                            $('#modal_post_chat_liking').modal('show')
                        });

                        prepender.find('.reading_like').on('click', function (e) {

                            e.preventDefault()
                            if ($('#user_id').html() === '') {
                                $('#modal_need_login').modal('show')
                                return false;
                            }
                            var post_chat_id = $(this).attr('data-u')

                            $.ajax({
                                url: '/re/post/chat/like/', type: 'post', dataType: 'json', cache: false,
                                data: {
                                    post_chat_id: post_chat_id,
                                },
                                success: function (data) {
                                    if (data.res === 1) {
                                        var has_k = $('#reading_like_count_' + post_chat_id).html()

                                        if (data.liked === true) {
                                            if (!(has_k.includes('k'))) {
                                                $('#reading_like_count_' + post_chat_id).html(parseInt(has_k) + 1)
                                            }
                                            $('#reading_like_span_' + post_chat_id).removeClass('glyphicon-heart-empty')
                                            $('#reading_like_span_' + post_chat_id).addClass('glyphicon-heart')
                                        } else {
                                            if (!(has_k.includes('k'))) {
                                                $('#reading_like_count_' + post_chat_id).html(parseInt(has_k) - 1)
                                            }
                                            $('#reading_like_span_' + post_chat_id).removeClass('glyphicon-heart')
                                            $('#reading_like_span_' + post_chat_id).addClass('glyphicon-heart-empty')
                                        }
                                    }
                                }
                            })

                        });


                        $('#modal_reading_chat').append(prepender)
                        $(".modal_reading_chat").animate({scrollTop: $('.modal_reading_chat').prop("scrollHeight")}, 500);
                        $('#you_say_form_textarea').val('')
                    }


                }
            })
            return false;

        }

    })

    $('#you_say_form_btn').click(function (e) {
        e.preventDefault()
        if ($('#user_id').html() === '') {
            $('#modal_need_login').modal('show')
            return false;
        }

        var reading_post_id = $('#reading_post_id').html()
        var reading_post_profile_photo = $('#reading_post_profile_photo').html()
        var reading_post_profile_name = $('#reading_post_profile_name').html()

        var text = $('#you_say_form_textarea').val()
        if (text.trim() === '') {
            return false;
        }
        $.ajax({
            url: '/re/post/chat/add/say/', type: 'post', dataType: 'json', cache: false,
            data: {
                post_id: reading_post_id,
                post_chat_id: $('#reading_post_chat_last_id').html(),
                text: text,
            },
            success: function (data) {
                if (data.res === 1) {
                    var prepender, align, profile_photo, chat_content, like, like_count, rest_messages;
                    $('#reading_post_chat_last_id').html(data.post_chat_id)

                    like_count = 0

                    var heart;
                    heart = 'glyphicon-heart-empty'

                    rest_messages = ''

                    like = '<a href=""><span class="glyphicon ' + heart + ' reading_like" id="reading_like_span_' + data.post_chat_id + '" data-u="' + data.post_chat_id + '"></span></a><span class="reading_like_text"> </span><a href=""><span class="reading_like_text" id="reading_like_count_' + data.post_chat_id + '">' + like_count + '</span></a>'

                    chat_content = '<div class="reading_chat_content_i">' +
                        '<div>' + data.text + like + '</div>' +
                        '</div>'

                    prepender = $('<div>' + chat_content + rest_messages + '</div>')
                    var last_id;

                    prepender.find('#reading_like_count_' + data.post_chat_id).on('click', function (e) {
                        e.preventDefault()
                        if ($('#user_id').html() === '') {
                            $('#modal_need_login').modal('show')
                            return false;
                        }
                        $('#clicked_post_chat_id').html(data.post_chat_id)
                        $('#modal_post_chat_liking').modal('show')
                    });

                    prepender.find('.reading_like').on('click', function (e) {

                        e.preventDefault()
                        if ($('#user_id').html() === '') {
                            $('#modal_need_login').modal('show')
                            return false;
                        }
                        var post_chat_id = $(this).attr('data-u')

                        $.ajax({
                            url: '/re/post/chat/like/', type: 'post', dataType: 'json', cache: false,
                            data: {
                                post_chat_id: post_chat_id,
                            },
                            success: function (data) {
                                if (data.res === 1) {
                                    var has_k = $('#reading_like_count_' + post_chat_id).html()

                                    if (data.liked === true) {
                                        if (!(has_k.includes('k'))) {
                                            $('#reading_like_count_' + post_chat_id).html(parseInt(has_k) + 1)
                                        }
                                        $('#reading_like_span_' + post_chat_id).removeClass('glyphicon-heart-empty')
                                        $('#reading_like_span_' + post_chat_id).addClass('glyphicon-heart')
                                    } else {
                                        if (!(has_k.includes('k'))) {
                                            $('#reading_like_count_' + post_chat_id).html(parseInt(has_k) - 1)
                                        }
                                        $('#reading_like_span_' + post_chat_id).removeClass('glyphicon-heart')
                                        $('#reading_like_span_' + post_chat_id).addClass('glyphicon-heart-empty')
                                    }
                                }
                            }
                        })

                    });


                    $('#modal_reading_chat').append(prepender)
                    $(".modal_reading_chat").animate({scrollTop: $('.modal_reading_chat').prop("scrollHeight")}, 500);
                    $('#you_say_form_textarea').val('')

                }


            }
        })
        return false;

    })

})
