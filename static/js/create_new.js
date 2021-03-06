$(function () {
    $('#whose').val('self')
    $('#title').val('off')
    $('#description').val('off')
    $('#open_close').val('open')
    $('#title_content').val('')
    $('#description_content').val('')
    $('#your_profile').click(function (e) {
        e.preventDefault()
        if ($(this).hasClass('choice_unselected')) {
            $(this).toggleClass('choice_selected choice_unselected')
        }
        if ($('#other_profile').hasClass('choice_selected')) {
            $('#other_profile').toggleClass('choice_selected choice_unselected')
        }
        if (!$('#name_fill').hasClass('hidden')) {
            $('#name_fill').toggleClass('hidden')
        }
        $('#whose').val('self')
    });
    $('#other_profile').click(function (e) {
        e.preventDefault()
        if ($(this).hasClass('choice_unselected')) {
            $(this).toggleClass('choice_selected choice_unselected')
        }
        if ($('#your_profile').hasClass('choice_selected')) {
            $('#your_profile').toggleClass('choice_selected choice_unselected')
        }
        if ($('#name_fill').hasClass('hidden')) {
            $('#name_fill').toggleClass('hidden')
        }
        $('#whose').val('other')
    })
    $('#title_not').click(function (e) {
        e.preventDefault()
        if ($(this).hasClass('choice_unselected')) {
            $(this).toggleClass('choice_selected choice_unselected')
        }
        if ($('#title_add').hasClass('choice_selected')) {
            $('#title_add').toggleClass('choice_selected choice_unselected')
        }

        if (!$('#title_fill').hasClass('hidden')) {
            $('#title_fill').toggleClass('hidden')
        }
        $('#title').val('off')

    });
    $('#title_add').click(function (e) {
        e.preventDefault()
        if ($(this).hasClass('choice_unselected')) {
            $(this).toggleClass('choice_selected choice_unselected')
        }
        if ($('#title_not').hasClass('choice_selected')) {
            $('#title_not').toggleClass('choice_selected choice_unselected')
        }
        if ($('#title_fill').hasClass('hidden')) {
            $('#title_fill').toggleClass('hidden')
        }
        $('#title').val('on')
    })
    $('#desc_not').click(function (e) {
        e.preventDefault()
        if ($(this).hasClass('choice_unselected')) {
            $(this).toggleClass('choice_selected choice_unselected')
        }
        if ($('#desc_add').hasClass('choice_selected')) {
            $('#desc_add').toggleClass('choice_selected choice_unselected')
        }

        if (!$('#desc_fill').hasClass('hidden')) {
            $('#desc_fill').toggleClass('hidden')
        }
        $('#description').val('off')
    });
    $('#desc_add').click(function (e) {
        e.preventDefault()
        if ($(this).hasClass('choice_unselected')) {
            $(this).toggleClass('choice_selected choice_unselected')
        }
        if ($('#desc_not').hasClass('choice_selected')) {
            $('#desc_not').toggleClass('choice_selected choice_unselected')
        }
        if ($('#desc_fill').hasClass('hidden')) {
            $('#desc_fill').toggleClass('hidden')
        }
        $('#description').val('on')
    })

    $('#open_close_open').click(function (e) {
        e.preventDefault()
        if ($(this).hasClass('choice_unselected')) {
            $(this).toggleClass('choice_selected choice_unselected')
        }
        if ($('#open_close_close').hasClass('choice_selected')) {
            $('#open_close_close').toggleClass('choice_selected choice_unselected')
        }
        $('#open_close').val('open')
    });
    $('#open_close_close').click(function (e) {
        e.preventDefault()
        if ($(this).hasClass('choice_unselected')) {
            $(this).toggleClass('choice_selected choice_unselected')
        }
        if ($('#open_close_open').hasClass('choice_selected')) {
            $('#open_close_open').toggleClass('choice_selected choice_unselected')
        }

        $('#open_close').val('close')
    })

})


var create_set = (function create_set() {
    return true;
});