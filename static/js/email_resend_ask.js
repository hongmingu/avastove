$(function () {

            $.ajax({
                url:'/accounts/email_ask/',
                type:'post',
                dataType:'json',
                cache:false,
                data:{
                    type:'ask'
                },
                success:function (data) {
                    if (data.res === 0){
                        var email_ask = '\n' +
                            '        <p class="h4">It\'s not activated yet</p>\n' +
                            '        <p class="h4"><a href="'+$('#div_email_ask').attr('data-cus')+'"><span class="clickable padding_5 pastel_bc3">Resend email</span></a> <a href="#"><span class="clickable padding_5 pastel_bc3" id="btn_email_ask_close">Close</span></a></p>'
                        $('#div_email_ask').append(email_ask);

                        $('#btn_email_ask_close').click(function (e) {
                            e.preventDefault();
                            $.ajax({
                                url:'/accounts/email_ask/',
                                type:'post',
                                dataType:'json',
                                cache:false,
                                data:{
                                    type:'close'
                                },
                                success:function (data) {
                                    if (data.res === 1){
                                        $('#div_email_ask').remove()
                                    }
                                }
                            });
                        });
                    }
                }
            });


        });