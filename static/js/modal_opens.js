
$(function () {
    $("#modal_post_follow").on("shown.bs.modal", function () {
        var height = $(window).height();
        $('.modal_follow_wrapper').css('max-height', height-120);
        $(window).on('resize', function(){

            if($(window).height() != height){
                height = $(window).height();
                $('.modal_follow_wrapper').css('max-height', height-120);
            }
        });
            var post_id = $('#clicked_post_id').html()

            $.ajax({url:'/re/post/follow/list/', type:'post', dataType:'json', cache:false,
                data:{
                    post_id: post_id,
                    next_id: $('#post_follow_next_id').html()
                },
                success:function (data) {
                    if (data.res === 1){
                        $.each(data.set, function (key, value) {
                            var appender = '<div class="profile_list_wrapper"><a href="/'+value.username+'/">\n' +
                                '<img class="img_small" src="'+value.photo+'">\n' +
                                '<span class="profile_list_username">'+value.username+'</span>\n' +
                                '</a></div>'
                            $('#modal_post_follow_list').append(appender)
                        })
                    }
                    if (data.next === null){
                        $('#post_follow_next_id').html('')
                        $('#modal_post_follow_more').addClass('hidden')
                    } else {
                        $('#post_follow_next_id').html(data.next)
                        $('#modal_post_follow_more').removeClass('hidden')
                    }

                }
            })
    }).on("hidden.bs.modal", function () {

            $('#modal_post_follow_list').empty()
            $('#post_follow_next_id').html('')
            $('#clicked_post_id').html('')
    })


    $("#modal_post_chat_rest_liking").on("shown.bs.modal", function () {
        var height = $(window).height();
        $('.modal_follow_wrapper').css('max-height', height-120);
        $(window).on('resize', function(){

            if($(window).height() != height){
                height = $(window).height();
                $('.modal_follow_wrapper').css('max-height', height-120);
            }
        });
            var post_chat_id = $('#clicked_post_chat_rest_id').html()

            $.ajax({url:'/re/post/chat/rest/like/list/', type:'post', dataType:'json', cache:false,
                data:{
                    post_chat_rest_id: post_chat_id,
                    next_id: $('#post_chat_rest_liking_next_id').html()
                },
                success:function (data) {
                    if (data.res === 1){
                        $.each(data.set, function (key, value) {
                            var appender = '<div class="profile_list_wrapper"><a href="/'+value.username+'/">\n' +
                                '<img class="img_small" src="'+value.photo+'">\n' +
                                '<span class="profile_list_username">'+value.username+'</span>\n' +
                                '</a></div>'
                            $('#modal_post_chat_rest_liking_list').append(appender)
                        })
                    }
                    if (data.next === null){
                        $('#post_chat_rest_liking_next_id').html('')
                        $('#modal_post_chat_rest_liking_more').addClass('hidden')
                    } else {
                        $('#post_chat_rest_liking_next_id').html(data.next)
                        $('#modal_post_chat_rest_liking_more').removeClass('hidden')
                    }

                }
            })
    }).on("hidden.bs.modal", function () {

            $('#modal_post_chat_rest_liking_list').empty()
            $('#post_chat_rest_liking_next_id').html('')
            $('#clicked_post_chat_rest_id').html('')
    })


    $("#modal_post_chat_liking").on("shown.bs.modal", function () {
        var height = $(window).height();
        $('.modal_follow_wrapper').css('max-height', height-120);
        $(window).on('resize', function(){

            if($(window).height() != height){
                height = $(window).height();
                $('.modal_follow_wrapper').css('max-height', height-120);
            }
        });
            var post_chat_id = $('#clicked_post_chat_id').html()

            $.ajax({url:'/re/post/chat/like/list/', type:'post', dataType:'json', cache:false,
                data:{
                    post_chat_id: post_chat_id,
                    next_id: $('#post_chat_liking_next_id').html()
                },
                success:function (data) {
                    if (data.res === 1){
                        $.each(data.set, function (key, value) {
                            var appender = '<div class="profile_list_wrapper"><a href="/'+value.username+'/">\n' +
                                '<img class="img_small" src="'+value.photo+'">\n' +
                                '<span class="profile_list_username">'+value.username+'</span>\n' +
                                '</a></div>'
                            $('#modal_post_chat_liking_list').append(appender)
                        })
                    }
                    if (data.next === null){
                        $('#post_chat_liking_next_id').html('')
                        $('#modal_post_chat_liking_more').addClass('hidden')
                    } else {
                        $('#post_chat_liking_next_id').html(data.next)
                        $('#modal_post_chat_liking_more').removeClass('hidden')
                    }

                }
            })
    }).on("hidden.bs.modal", function () {

            $('#modal_post_chat_liking_list').empty()
            $('#post_chat_liking_next_id').html('')
            $('#clicked_post_chat_id').html('')
    })


    $("#modal_post_liking").on("shown.bs.modal", function () {
    var height = $(window).height();
    $('.modal_follow_wrapper').css('max-height', height-120);
    $(window).on('resize', function(){

        if($(window).height() != height){
            height = $(window).height();
            $('.modal_follow_wrapper').css('max-height', height-120);
        }
    });
            var post_id = $('#reading_post_id').html()

            $.ajax({url:'/re/post/like/list/', type:'post', dataType:'json', cache:false,
                data:{
                    post_id: post_id,
                    next_id: $('#post_liking_next_id').html()
                },
                success:function (data) {
                    if (data.res === 1){
                        $.each(data.set, function (key, value) {
                            var appender = '<div class="profile_list_wrapper"><a href="/'+value.username+'/">\n' +
                                '<img class="img_small" src="'+value.photo+'">\n' +
                                '<span class="profile_list_username">'+value.username+'</span>\n' +
                                '</a></div>'
                            $('#modal_post_liking_list').append(appender)
                        })
                    }
                    if (data.next === null){
                        $('#post_liking_next_id').html('')
                        $('#modal_post_liking_more').addClass('hidden')
                    } else {
                        $('#post_liking_next_id').html(data.next)
                        $('#modal_post_liking_more').removeClass('hidden')
                    }

                }
            })
        }).on("hidden.bs.modal", function () {
            $('#modal_post_liking_list').empty()
            $('#post_liking_next_id').html('')
            $('#reading_post_id').html('')
        });

})
