$(function () {
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
            title_command = 'add'
        }
        if ($('#desc_discriminant').hasClass('hidden')) {
            desc_command = 'removed'
        } else {
            desc_command = 'add'
        }

        $.ajax({
            url: '/re/post/update/',
            type: 'post',
            dataType: 'json',
            cache: false,
            data: {
                post_id: $('#post_id').attr('data-u'),
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
})