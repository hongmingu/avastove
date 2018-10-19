    var modify_last_delete = function modify_last_delete(){
        $('.chat_preview_delete').addClass('hidden')
        if ($('.chat_preview_delete').last().hasClass('hidden')){
            console.log($('.chat_preview_delete').last().attr('data-u')+'has hidden')
            $('.chat_preview_delete').last().removeClass('hidden')
        }
    }
    var recent_post_chat;

$(function () {

    $('#go_to_main').click(function (e) {
        e.preventDefault()
        location.href='/'
    })
    var open;
    if ($('#just_created').attr('data-u') === 'on') {
        if ($('#open').hasClass('choice_unselected')) {
            $('#open').toggleClass('choice_selected choice_unselected')
        }
        if ($('#close').hasClass('choice_selected')) {
            $('#close').toggleClass('choice_selected choice_unselected')
        }
        open = 'open'

    } else {
        if ($('#current_open').attr('data-u') === 'open') {
            if ($('#open').hasClass('choice_unselected')) {
                $('#open').toggleClass('choice_selected choice_unselected')
            }
            if ($('#close').hasClass('choice_selected')) {
                $('#close').toggleClass('choice_selected choice_unselected')
            }
            open = 'open'

        } else {
            if ($('#close').hasClass('choice_unselected')) {
                $('#close').toggleClass('choice_selected choice_unselected')
            }
            if ($('#open').hasClass('choice_selected')) {
                $('#open').toggleClass('choice_selected choice_unselected')
            }
            open = 'close'
        }
    }
    $('#open').click(function (e) {
        e.preventDefault()
        if ($(this).hasClass('choice_unselected')) {
            $(this).toggleClass('choice_selected choice_unselected')
        }
        if ($('#close').hasClass('choice_selected')) {
            $('#close').toggleClass('choice_selected choice_unselected')
        }
        open = 'open'
    });
    $('#close').click(function (e) {
        e.preventDefault()
        if ($(this).hasClass('choice_unselected')) {
            $(this).toggleClass('choice_selected choice_unselected')
        }
        if ($('#open').hasClass('choice_selected')) {
            $('#open').toggleClass('choice_selected choice_unselected')
        }
        open = 'close'
    })


    $('#ok').click(function (e) {
        e.preventDefault()

        var title_command, desc_command;

        if ($('#title_discriminant').hasClass('hidden')) {
            title_command = 'removed'
        } else {
            if($('#title_input').val().replace(/ /g,'')===''){
                title_command = 'removed'
            } else {
                title_command = 'add'
            }
        }
        if ($('#desc_discriminant').hasClass('hidden')) {
            desc_command = 'removed'
        } else {
            if($('#desc_input').val().replace(/ /g,'')===''){
                desc_command = 'removed'
            } else {
                desc_command = 'add'
            }
        }

        $.ajax({
            url: '/re/post/update/',
            type: 'post',
            dataType: 'json',
            cache: false,
            data: {
                post_id: $('#post_id').html(),
                open: open,
                title_command: title_command,
                desc_command: desc_command,
                title: $('#title_input').val(),
                description: $('#desc_input').val(),
            },
            success: function (data) {
                if (data.res === 1) {
                    location.reload()
                }
            }
        });
    })
    $('.title_toggle').click(function (e) {
        e.preventDefault()
        $('.div_title').toggleClass('hidden')
    });
    $('.desc_toggle').click(function (e) {
        e.preventDefault()
        $('.div_desc').toggleClass('hidden')
    })

    $('#profile_name_change').click(function (e) {
        e.preventDefault()
        var name;
        name = $('#profile_name_input').val()
        if (name.replace(/ /g,'')===''){
            $('#name_clue').html('name cannot be empty').css('color', 'red')
            return false
        }
        if (!(1 <= name.length && name.length <= 30)) {
            $('#name_clue').html('1 < name length < 1000').css('color', 'red')
            return false
        }

        $.ajax({
            url: '/re/post/update/profile/name/',
            type: 'post',
            dataType: 'json',
            cache: false,
            data: {
                post_id: $('#post_id').html(),
                name: $('#profile_name_input').val(),
            },
            success: function (data) {
                if (data.res === 1) {
                    location.reload()
                }
            }
        });
    })

    var you_say = 'you';
        $('#you_say').click(function (e) {
            e.preventDefault()
            if ($(this).hasClass('choice_unselected')) {
                $(this).toggleClass('choice_selected choice_unselected')
            }
            if ($('#someone_says').hasClass('choice_selected')) {
                $('#someone_says').toggleClass('choice_selected choice_unselected')
            }
            you_say = 'you'
        });
        $('#someone_says').click(function (e) {
            e.preventDefault()
            if ($(this).hasClass('choice_unselected')) {
                $(this).toggleClass('choice_selected choice_unselected')
            }
            if ($('#you_say').hasClass('choice_selected')) {
                $('#you_say').toggleClass('choice_selected choice_unselected')
            }
            you_say = 'someone'
        })


        $('#post_chat_textarea').on("keypress", function (e) {
            /* ENTER PRESSED*/
            if (e.keyCode == 13 && !e.shiftKey) {
                var text = $('#post_chat_textarea').val()
                if(text === ''){
                    return false;
                }
                if(text.replace(/ /g,'')===''){
                    return false;
                }

                $.ajax({
                    url: '/re/create/new/text/',
                    type: 'post',
                    dataType: 'json',
                    cache: false,
                    data: {
                        you_say: you_say,
                        text: text,
                        post_id: $('#post_id').attr('data-u')
                    },
                    success: function (data) {
                        if (data.res === 1) {
                            if (data.content.you_say === true) {
                                var chat_preview = $('<div class="chat_preview_wrapper" id="chat_'+data.content.id+'"align="left">\n' +
                                    '<div class="chat_preview_size">\n' +
                                    '<div><span class="chat_preview_name">You</span></div>\n' +
                                    '<div class="chat_preview_you_saying"><span class="chat_preview_you_saying_text">' + data.content.text + '</span></div>\n' +
                                    '<div class="chat_preview_delete_wrapper" align="left"><a href=""><span class="chat_preview_delete clickable hidden" data-u="'+data.content.id+'" >delete</span></a></div>\n' +
                                    '</div>\n' +
                                    '</div>')
                                chat_preview.find('.chat_preview_delete').on('click', function (e) {
                                    e.preventDefault()
                                    var id = $(this).attr('data-u')
                                    $.ajax({
                                        url: '/re/post/chat/remove/', type: 'post', dataType:'json', cache: false,
                                        data: {
                                            post_chat_id: id,
                                        },
                                        success: function (data) {
                                            if (data.res === 1){
                                                $('#chat_'+id).remove()
                                                $.when($('#chat_'+id).remove()).then(modify_last_delete());
                                            }
                                        }
                                    })
                                })
                                $('#chat_preview').append(chat_preview)
                                modify_last_delete()

                            } else {
                                var chat_preview = $('<div class="chat_preview_wrapper" id="chat_'+data.content.id+'" align="right">\n' +
                                    '<div class="chat_preview_size">\n' +
                                    '<div><span class="chat_preview_name">Someone</span></div>\n' +
                                    '<div class="chat_preview_someone_saying"><span class="chat_preview_someone_saying_text">' + data.content.text + '</span></div>\n' +
                                    '<div class="chat_preview_delete_wrapper" align="right"><a href=""><span class="chat_preview_delete clickable hidden" data-u="'+data.content.id+'" >delete</span></a></div>\n' +
                                    '</div>\n' +
                                    '</div>')
                                chat_preview.find('.chat_preview_delete').on('click', function (e) {
                                    e.preventDefault()
                                    var id = $(this).attr('data-u')
                                    $.ajax({
                                        url: '/re/post/chat/remove/', type: 'post', dataType:'json', cache: false,
                                        data: {
                                            post_id: id,
                                        },
                                        success: function (data) {
                                            if (data.res === 1){
                                                $('#chat_'+id).remove()
                                                $.when($('#chat_'+id).remove()).then(modify_last_delete());
                                            }
                                        }
                                    })
                                })
                                $('#chat_preview').append(chat_preview)
                                modify_last_delete()

                            }
                        }

                        var objDiv = document.getElementById("chat_preview_wrapper");
                        objDiv.scrollTop = objDiv.scrollHeight;
                    }
                });

                $('#post_chat_textarea').val('');
                return false;
            }
        });
        $('#btn_add ').click(function (e) {
            e.preventDefault()
            var text = $('#post_chat_textarea').val()
            if(text === ''){
                return false;
            }
            if(text.replace(/ /g,'')===''){
                return false;
            }
            $.ajax({
                url: '/re/create/new/text/',
                type: 'post',
                dataType: 'json',
                cache: false,
                data: {
                    you_say: you_say,
                    text: text,
                    post_id: $('#post_id').attr('data-u')
                },
                success: function (data) {
                    if (data.res === 1) {
                        if (data.content.you_say === true) {
                            var chat_preview = $('<div class="chat_preview_wrapper" id="chat_'+data.content.id+'"align="left">\n' +
                                '<div class="chat_preview_size">\n' +
                                '<div><span class="chat_preview_name">You</span></div>\n' +
                                '<div class="chat_preview_you_saying"><span class="chat_preview_you_saying_text">' + data.content.text + '</span></div>\n' +
                                '<div class="chat_preview_delete_wrapper" align="left"><a href=""><span class="chat_preview_delete clickable hidden" data-u="'+data.content.id+'" >delete</span></a></div>\n' +
                                '</div>\n' +
                                '</div>')
                            chat_preview.find('.chat_preview_delete').on('click', function (e) {
                                e.preventDefault()
                                var id = $(this).attr('data-u')
                                $.ajax({
                                    url: '/re/post/chat/remove/', type: 'post', dataType:'json', cache: false,
                                    data: {
                                        post_chat_id: id,
                                    },
                                    success: function (data) {
                                        if (data.res === 1){
                                            $('#chat_'+id).remove()
                                            $.when($('#chat_'+id).remove()).then(modify_last_delete());
                                        }
                                    }
                                })
                            })
                            $('#chat_preview').append(chat_preview)
                            modify_last_delete()

                        } else {
                            var chat_preview = $('<div class="chat_preview_wrapper" id="chat_'+data.content.id+'" align="right">\n' +
                                '<div class="chat_preview_size">\n' +
                                '<div><span class="chat_preview_name">Someone</span></div>\n' +
                                '<div class="chat_preview_someone_saying"><span class="chat_preview_someone_saying_text">' + data.content.text + '</span></div>\n' +
                                '<div class="chat_preview_delete_wrapper" align="right"><a href=""><span class="chat_preview_delete clickable hidden" data-u="'+data.content.id+'" >delete</span></a></div>\n' +
                                '</div>\n' +
                                '</div>')
                            chat_preview.find('.chat_preview_delete').on('click', function (e) {
                                e.preventDefault()
                                var id = $(this).attr('data-u')
                                $.ajax({
                                    url: '/re/post/chat/remove/', type: 'post', dataType:'json', cache: false,
                                    data: {
                                        post_chat_id: id,
                                    },
                                    success: function (data) {
                                        if (data.res === 1){
                                            $('#chat_'+id).remove()
                                            $.when($('#chat_'+id).remove()).then(modify_last_delete());
                                        }
                                    }
                                })
                            })
                            $('#chat_preview').append(chat_preview)
                            modify_last_delete()

                        }
                    }

                    var objDiv = document.getElementById("chat_preview_wrapper");
                    objDiv.scrollTop = objDiv.scrollHeight;
                }
            });

            $('#post_chat_textarea').val('');
            return false;

        });


        $('#add_photo').click(function (e) {
            e.preventDefault();
            $('#input_chat_file').click()
        })

        $('#input_chat_file').change(function () {
            if (this.files && this.files[0]) {
                if (this.files[0].size > (1048576 * 10)) {
                    var agent = navigator.userAgent.toLowerCase();

                    if ((navigator.appName == 'Netscape' && navigator.userAgent.search('Trident') != -1) || (agent.indexOf("msie") != -1)) {
                        // ie 일때 input[type=file] init.
                        $('#input_chat_file').replaceWith($('#input_chat_file').clone(true));
                    } else {
                        //other browser 일때 input[type=file] init.
                        $('#input_chat_file').val("");
                    }
                    alert('File size can\'t exceed 10m');
                    return;
                }
                var reader = new FileReader();
                reader.onload = function (e) {
                    $("#img_chat").attr("src", e.target.result);
                    $("#img_chat_hidden").attr("src", e.target.result);
                    $("#modal_chat").modal("show");
                };
                reader.readAsDataURL(this.files[0]);
            }
        });

        var image;
        var cropper
        var save_this;
        $("#modal_chat").on("shown.bs.modal", function () {
            image = document.getElementById('img_chat_hidden');
            cropper = new Cropper(image,);
            var rotate_from = cropper.getData()
            $('#img_chat').each(function () {
                var deg = rotate_from['rotate'];
                var rotate = 'rotate(' + deg + 'deg)';
                save_this = $(this)

                if (deg % 180 === 90 || deg % 180 === -90) {
                    if (save_this.parent().height() !== save_this.width()) {
                        save_this.parent().css('height', save_this.width())
                        save_this.css('margin-top', (save_this.width() - save_this.height()) / 2)
                    }
                } else {
                    if (save_this.parent().height() !== save_this.height()) {
                        save_this.parent().css('height', save_this.height())
                        save_this.css('margin-top', 0)
                    }
                }
                save_this.css({
                    '-webkit-transform': rotate,
                    '-moz-transform': rotate,
                    '-o-transform': rotate,
                    '-ms-transform': rotate,
                    'transform': rotate
                });
                //사소한 에러는 나중에 신경쓰고 우선 이걸 포스트해서 받아와서 챗 창에 띄우는 걸 짜자.
            });

        }).on("hidden.bs.modal", function () {

            cropper.destroy();
            var agent = navigator.userAgent.toLowerCase();

            if ((navigator.appName == 'Netscape' && navigator.userAgent.search('Trident') != -1) || (agent.indexOf("msie") != -1)) {
                // ie 일때 input[type=file] init.
                $('#input_chat_file').replaceWith($('#input_chat_file').clone(true));
            } else {
                //other browser 일때 input[type=file] init.
                $('#input_chat_file').val("");
            }
        });

        $(".chat-upload").click(function () {
            var cropData = cropper.getData();

            var form_file = $('#chat_upload')[0];
            var form_data = new FormData(form_file);
            form_data.append('rotate', cropData["rotate"]);
            form_data.append('you_say', you_say);
            form_data.append('post_id', $('#post_id').attr('data-u'));

            $.ajax({
                url: '/re/create/new/chat_photo/',
                type: 'post',
                dataType: 'json',
                cache: false,
                processData: false,
                contentType: false,
                data: form_data,
                success: function (data) {
                    if (data.res === 1) {
                        if (data.content.you_say === true) {
                            var chat_preview = $('<div class="chat_preview_wrapper" id="chat_'+data.content.id+'"align="left">\n' +
                                '<div class="chat_preview_size">\n' +
                                '<div><span class="chat_preview_name">You</span></div>\n' +
                                '<div align="right"><img class="chat_preview_img" src="'+data.content.url+'"></div>' +
                                '<div class="chat_preview_delete_wrapper" align="left"><a href=""><span class="chat_preview_delete clickable hidden" data-u="'+data.content.id+'" >delete</span></a></div>\n' +
                                '</div>\n' +
                                '</div>')
                            chat_preview.find('.chat_preview_delete').on('click', function (e) {
                                e.preventDefault()
                                var id = $(this).attr('data-u')
                                $.ajax({
                                    url: '/re/post/chat/remove/', type: 'post', dataType:'json', cache: false,
                                    data: {
                                        post_chat_id: id,
                                    },
                                    success: function (data) {
                                        if (data.res === 1) {
                                            $('#chat_' + id).remove()
                                            $.when($('#chat_' + id).remove()).then(modify_last_delete());
                                        }
                                    }
                                })
                            })
                            $('#chat_preview').append(chat_preview)
                            modify_last_delete()

                        } else {
                            var chat_preview = $('<div class="chat_preview_wrapper" id="chat_'+data.content.id+'" align="right">\n' +
                                '<div class="chat_preview_size">\n' +
                                '<div><span class="chat_preview_name">Someone</span></div>\n' +
                                '<div align="left"><img class="chat_preview_img" src="'+data.content.url+'"></div>' +
                                '<div class="chat_preview_delete_wrapper" align="right"><a href=""><span class="chat_preview_delete clickable hidden" data-u="'+data.content.id+'" >delete</span></a></div>\n' +
                                '</div>\n' +
                                '</div>')
                            chat_preview.find('.chat_preview_delete').on('click', function (e) {
                                e.preventDefault()
                                var id = $(this).attr('data-u')
                                $.ajax({
                                    url: '/re/post/chat/remove/', type: 'post', dataType:'json', cache: false,
                                    data: {
                                        post_chat_id: id,
                                    },
                                    success: function (data) {
                                        if (data.res === 1){
                                            $('#chat_'+id).remove()
                                            $.when($('#chat_'+id).remove()).then(modify_last_delete());
                                        }
                                    }
                                })
                            })
                            $('#chat_preview').append(chat_preview)
                            modify_last_delete()

                        }
                    }

                    var objDiv = document.getElementById("chat_preview_wrapper");
                    objDiv.scrollTop = objDiv.scrollHeight;
                    $("#modal_chat").modal("hide");
                    return false;
                }
            });
        });


        $.ajax({
                                    url: '/re/post/chat/modify/populate/', type: 'post', dataType:'json', cache: false,
                                    data: {
                                        post_id: $('#post_id').html()
                                    },
                                    success: function (data) {
                                        var object = data.set
                                        if (data.res === 1) {
                                            var there_were_starting = false;
                                            $.each(JSON.parse(object), function (key, value) {
                                                recent_post_chat = value.id
                                                switch (value.kind) {
                                                    case 'start':

                                                        $('#chat_preview').prepend('<div class="chat_preview_wrapper" align="center">\n' +
                                                            '<div class="chat_preview_first_chat">Conversation begin</div>\n' +
                                                            '</div>\n');
                                                        there_were_starting = true
                                                        break;
                                                    case 'text':
                                                        if (value.you_say === true) {
                                                            var chat_preview = $('<div class="chat_preview_wrapper" id="chat_' + value.id + '"align="left">\n' +
                                                                '<div class="chat_preview_size">\n' +
                                                                '<div><span class="chat_preview_name">You</span></div>\n' +
                                                                '<div class="chat_preview_you_saying"><span class="chat_preview_you_saying_text">' + value.text + '</span></div>\n' +
                                                                '<div class="chat_preview_delete_wrapper" align="left"><a href=""><span class="chat_preview_delete clickable hidden" data-u="' + value.id + '" >delete</span></a></div>\n' +
                                                                '</div>\n' +
                                                                '</div>')
                                                            chat_preview.find('.chat_preview_delete').on('click', function (e) {
                                                                e.preventDefault()
                                                                var id = $(this).attr('data-u')
                                                                $.ajax({
                                                                    url: '/re/post/chat/remove/',
                                                                    type: 'post',
                                                                    dataType: 'json',
                                                                    cache: false,
                                                                    data: {
                                                                        post_chat_id: id,
                                                                    },
                                                                    success: function (data) {
                                                                        if (data.res === 1) {
                                                                            $('#chat_' + id).remove()
                                                                            $.when($('#chat_' + id).remove()).then(modify_last_delete());
                                                                        }
                                                                    }
                                                                })
                                                            })
                                                            $('#chat_preview').prepend(chat_preview)
                                                            modify_last_delete()

                                                        } else {
                                                            var chat_preview = $('<div class="chat_preview_wrapper" id="chat_' + value.id + '" align="right">\n' +
                                                                '<div class="chat_preview_size">\n' +
                                                                '<div><span class="chat_preview_name">Someone</span></div>\n' +
                                                                '<div class="chat_preview_someone_saying"><span class="chat_preview_someone_saying_text">' + value.text + '</span></div>\n' +
                                                                '<div class="chat_preview_delete_wrapper" align="right"><a href=""><span class="chat_preview_delete clickable hidden" data-u="' + value.id + '" >delete</span></a></div>\n' +
                                                                '</div>\n' +
                                                                '</div>')
                                                            chat_preview.find('.chat_preview_delete').on('click', function (e) {
                                                                e.preventDefault()
                                                                var id = $(this).attr('data-u')
                                                                $.ajax({
                                                                    url: '/re/post/chat/remove/',
                                                                    type: 'post',
                                                                    dataType: 'json',
                                                                    cache: false,
                                                                    data: {
                                                                        post_chat_id: id,
                                                                    },
                                                                    success: function (data) {
                                                                        if (data.res === 1) {
                                                                            $('#chat_' + id).remove()
                                                                            $.when($('#chat_' + id).remove()).then(modify_last_delete());
                                                                        }
                                                                    }
                                                                })
                                                            })
                                                            $('#chat_preview').prepend(chat_preview)
                                                            modify_last_delete()

                                                        }
                                                        $('#chat_preview')
                                                        break;
                                                    case 'photo':
                                                        if (value.you_say === true) {
                                                            var chat_preview = $('<div class="chat_preview_wrapper" id="chat_' + value.id + '"align="left">\n' +
                                                                '<div class="chat_preview_size">\n' +
                                                                '<div><span class="chat_preview_name">You</span></div>\n' +
                                                                '<div align="right"><img class="chat_preview_img" src="' + value.url + '"></div>' +
                                                                '<div class="chat_preview_delete_wrapper" align="left"><a href=""><span class="chat_preview_delete clickable hidden" data-u="' + value.id + '" >delete</span></a></div>\n' +
                                                                '</div>\n' +
                                                                '</div>')
                                                            chat_preview.find('.chat_preview_delete').on('click', function (e) {
                                                                e.preventDefault()
                                                                var id = $(this).attr('data-u')
                                                                $.ajax({
                                                                    url: '/re/post/chat/remove/',
                                                                    type: 'post',
                                                                    dataType: 'json',
                                                                    cache: false,
                                                                    data: {
                                                                        post_chat_id: id,
                                                                    },
                                                                    success: function (data) {
                                                                        if (data.res === 1) {
                                                                            $('#chat_' + id).remove()
                                                                            $.when($('#chat_' + id).remove()).then(modify_last_delete());
                                                                        }
                                                                    }
                                                                })
                                                            })
                                                            $('#chat_preview').prepend(chat_preview)
                                                            modify_last_delete()

                                                        } else {
                                                            var chat_preview = $('<div class="chat_preview_wrapper" id="chat_' + value.id + '" align="right">\n' +
                                                                '<div class="chat_preview_size">\n' +
                                                                '<div><span class="chat_preview_name">Someone</span></div>\n' +
                                                                '<div align="left"><img class="chat_preview_img" src="' + value.url + '"></div>' +
                                                                '<div class="chat_preview_delete_wrapper" align="right"><a href=""><span class="chat_preview_delete clickable hidden" data-u="' + value.id + '" >delete</span></a></div>\n' +
                                                                '</div>\n' +
                                                                '</div>')
                                                            chat_preview.find('.chat_preview_delete').on('click', function (e) {
                                                                e.preventDefault()
                                                                var id = $(this).attr('data-u')
                                                                $.ajax({
                                                                    url: '/re/post/chat/remove/',
                                                                    type: 'post',
                                                                    dataType: 'json',
                                                                    cache: false,
                                                                    data: {
                                                                        post_id: $('#post_id').attr('data-u'),
                                                                    },
                                                                    success: function (data) {
                                                                        if (data.res === 1) {
                                                                            $('#chat_' + id).remove()
                                                                            $.when($('#chat_' + id).remove()).then(modify_last_delete());
                                                                        }
                                                                    }
                                                                })
                                                            })
                                                            $('#chat_preview').prepend(chat_preview)
                                                            modify_last_delete()

                                                        }
                                                        break;
                                                    default:
                                                        return;
                                                }

                                            })
                                            if (!(there_were_starting)){
                                                if($('#more_load').hasClass('hidden')){
                                                    $('#more_load').removeClass('hidden')
                                                }
                                            } else {
                                                if(!($('#more_load').hasClass('hidden'))){
                                                    $('#more_load').addClass('hidden')
                                                }
                                            }
                                        }
                                    }
                                })
                                $('#more_load').click(function (e) {
                                    e.preventDefault()
                                    $.ajax({
                                        url: '/re/post/chat/more/load/', type: 'post', dataType: 'json', cache: false,
                                        data: {
                                            post_id: $('#post_id').attr('data-u'),
                                            post_chat_id: recent_post_chat,
                                        },
                                        success: function (data) {
                                            var object = data.set
                                            if (data.res === 1) {
                                                var there_were_starting = false;
                                                $.each(JSON.parse(object), function (key, value) {
                                                    recent_post_chat = value.id
                                                    switch (value.kind) {
                                                        case 'start':

                                                            $('#chat_preview').prepend('<div class="chat_preview_wrapper" align="center">\n' +
                                                                '<div class="chat_preview_first_chat">Conversation begin</div>\n' +
                                                                '</div>\n');
                                                            there_were_starting = true
                                                            break;
                                                        case 'text':
                                                            if (value.you_say === true) {
                                                                var chat_preview = $('<div class="chat_preview_wrapper" id="chat_' + value.id + '"align="left">\n' +
                                                                    '<div class="chat_preview_size">\n' +
                                                                    '<div><span class="chat_preview_name">You</span></div>\n' +
                                                                    '<div class="chat_preview_you_saying"><span class="chat_preview_you_saying_text">' + value.text + '</span></div>\n' +
                                                                    '<div class="chat_preview_delete_wrapper" align="left"><a href=""><span class="chat_preview_delete clickable hidden" data-u="' + value.id + '" >delete</span></a></div>\n' +
                                                                    '</div>\n' +
                                                                    '</div>')
                                                                chat_preview.find('.chat_preview_delete').on('click', function (e) {
                                                                    e.preventDefault()
                                                                    var id = $(this).attr('data-u')
                                                                    $.ajax({
                                                                        url: '/re/post/chat/remove/',
                                                                        type: 'post',
                                                                        dataType: 'json',
                                                                        cache: false,
                                                                        data: {
                                                                            post_chat_id: id,
                                                                        },
                                                                        success: function (data) {
                                                                            if (data.res === 1) {
                                                                                $('#chat_' + id).remove()
                                                                                $.when($('#chat_' + id).remove()).then(modify_last_delete());
                                                                            }
                                                                        }
                                                                    })
                                                                })
                                                                $('#chat_preview').prepend(chat_preview)
                                                                modify_last_delete()

                                                            } else {
                                                                var chat_preview = $('<div class="chat_preview_wrapper" id="chat_' + value.id + '" align="right">\n' +
                                                                    '<div class="chat_preview_size">\n' +
                                                                    '<div><span class="chat_preview_name">Someone</span></div>\n' +
                                                                    '<div class="chat_preview_someone_saying"><span class="chat_preview_someone_saying_text">' + value.text + '</span></div>\n' +
                                                                    '<div class="chat_preview_delete_wrapper" align="right"><a href=""><span class="chat_preview_delete clickable hidden" data-u="' + value.id + '" >delete</span></a></div>\n' +
                                                                    '</div>\n' +
                                                                    '</div>')
                                                                chat_preview.find('.chat_preview_delete').on('click', function (e) {
                                                                    e.preventDefault()
                                                                    var id = $(this).attr('data-u')
                                                                    $.ajax({
                                                                        url: '/re/post/chat/remove/',
                                                                        type: 'post',
                                                                        dataType: 'json',
                                                                        cache: false,
                                                                        data: {
                                                                            post_chat_id: id,
                                                                        },
                                                                        success: function (data) {
                                                                            if (data.res === 1) {
                                                                                $('#chat_' + id).remove()
                                                                                $.when($('#chat_' + id).remove()).then(modify_last_delete());
                                                                            }
                                                                        }
                                                                    })
                                                                })
                                                                $('#chat_preview').prepend(chat_preview)
                                                                modify_last_delete()

                                                            }
                                                            break;
                                                        case 'photo':
                                                            if (value.you_say === true) {
                                                                var chat_preview = $('<div class="chat_preview_wrapper" id="chat_' + value.id + '"align="left">\n' +
                                                                    '<div class="chat_preview_size">\n' +
                                                                    '<div><span class="chat_preview_name">You</span></div>\n' +
                                                                    '<div align="right"><img class="chat_preview_img" src="' + value.url + '"></div>' +
                                                                    '<div class="chat_preview_delete_wrapper" align="left"><a href=""><span class="chat_preview_delete clickable hidden" data-u="' + value.id + '" >delete</span></a></div>\n' +
                                                                    '</div>\n' +
                                                                    '</div>')
                                                                chat_preview.find('.chat_preview_delete').on('click', function (e) {
                                                                    e.preventDefault()
                                                                    var id = $(this).attr('data-u')
                                                                    $.ajax({
                                                                        url: '/re/post/chat/remove/',
                                                                        type: 'post',
                                                                        dataType: 'json',
                                                                        cache: false,
                                                                        data: {
                                                                            post_chat_id: id,
                                                                        },
                                                                        success: function (data) {
                                                                            if (data.res === 1) {
                                                                                $('#chat_' + id).remove()
                                                                                $.when($('#chat_' + id).remove()).then(modify_last_delete());
                                                                            }
                                                                        }
                                                                    })
                                                                })
                                                                $('#chat_preview').prepend(chat_preview)
                                                                modify_last_delete()


                                                            } else {
                                                                var chat_preview = $('<div class="chat_preview_wrapper" id="chat_' + value.id + '" align="right">\n' +
                                                                    '<div class="chat_preview_size">\n' +
                                                                    '<div><span class="chat_preview_name">Someone</span></div>\n' +
                                                                    '<div align="left"><img class="chat_preview_img" src="' + value.url + '"></div>' +
                                                                    '<div class="chat_preview_delete_wrapper" align="right"><a href=""><span class="chat_preview_delete clickable hidden" data-u="' + value.id + '" >delete</span></a></div>\n' +
                                                                    '</div>\n' +
                                                                    '</div>')
                                                                chat_preview.find('.chat_preview_delete').on('click', function (e) {
                                                                    e.preventDefault()
                                                                    var id = $(this).attr('data-u')
                                                                    $.ajax({
                                                                        url: '/re/post/chat/remove/',
                                                                        type: 'post',
                                                                        dataType: 'json',
                                                                        cache: false,
                                                                        data: {
                                                                            post_id: $('#post_id').attr('data-u'),
                                                                        },
                                                                        success: function (data) {
                                                                            if (data.res === 1) {
                                                                                $('#chat_' + id).remove()
                                                                                $.when($('#chat_' + id).remove()).then(modify_last_delete());
                                                                            }
                                                                        }
                                                                    })
                                                                })
                                                                $('#chat_preview').prepend(chat_preview)
                                                                modify_last_delete()

                                                            }
                                                            break;
                                                        default:
                                                            return;
                                                    }

                                                })
                                                if (!(there_were_starting)){
                                                    if($('#more_load').hasClass('hidden')){
                                                        $('#more_load').removeClass('hidden')
                                                    }
                                                } else {
                                                    if(!($('#more_load').hasClass('hidden'))){
                                                        $('#more_load').addClass('hidden')
                                                    }
                                                }
                                            }
                                        }
                                    })
                                })
})