$(function () {
    if(!($('#user_id').html()==='')){
        $.ajax({
            url: '/re/nav/badge/populate/', type: 'post', dataType: 'json', cache: false,
            data: {
            },
            success: function (data) {
                if (data.res === 1){
                    if(data.notice_count > 0){
                        $('#badge_note').html(data.notice_count)
                    }
                }
            }
        })
    }
})