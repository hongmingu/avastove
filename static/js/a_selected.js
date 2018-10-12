    $(function () {
        var page_kind = $('#page_kind').html();
        if (page_kind === 'home') {
            $('#a_home').addClass('a_selected');
        } else if (page_kind === 'feed') {
            $('#a_feed').addClass('a_selected');
        } else if (page_kind === 'user') {
            $('#a_user').addClass('a_selected');
        } else if (page_kind === 'note') {
            $('#a_note').addClass('a_selected');
        }
    });