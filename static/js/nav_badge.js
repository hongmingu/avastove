$(function () {
        $('.nav_badge').each(function () {
            $(this).css({
                'top': $($(this).attr('data-u')).offset().top,
                'left': $($(this).attr('data-u')).offset().left,
            })
        });
        var width = $(window).width();

        $(window).on('resize', function(){
            if($(this).width() != width){
                width = $(this).width();
                if(768<=width){
                    $('.nav_badge').each(function () {
                        $(this).css({
                            'top': $($(this).attr('data-u')).offset().top,
                            'left': $($(this).attr('data-u')).offset().left,
                        })
                    })
                } else if (343<=width && width<768) {

                    $('.nav_badge').each(function () {
                        $(this).css({
                            'top': $($(this).attr('data-u')).offset().top,
                            'left': $($(this).attr('data-u')).offset().left,
                        })
                    })
                } else if (width<343) {

                    $('.nav_badge').each(function () {
                        $(this).css({
                            'top': $($(this).attr('data-u')).offset().top,
                            'left': $($(this).attr('data-u')).offset().left,
                        })
                    })
                }
            }
        });

    });
