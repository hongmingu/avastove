$(function () {
    var height = $(window).height();
    $('#modal_reading_post_content').css('height', height-16);
    $('#modal_reading_chat').css('height', height-16-70-35-20)
    $(window).on('resize', function(){

        if($(window).height() != height){
            height = $(window).height();
            $('#modal_reading_post_content').css('height', height-16);
            $('#modal_reading_chat').css('height', height-16-70-35-20)
        }
    });
})