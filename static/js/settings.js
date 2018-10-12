    $(function () {
    $('#span_base_reset').click(function () {
        $("#modal_base_reset").modal("show");
    });
    $('#btn_base_reset_ok').click(function () {
            $.ajax({
            url:'/re_settings/ajax/upload_user_photo/',
            type:'post',
            dataType:'json',
            cache:false,
            data:{
                remove:'remove'
            },
            success:function (data) {
                $('#img_300').attr('src', '/media/default/default_photo_300.png')
                $("#modal_base_reset").modal("hide");

            }
        });
    });

$('#span_change_photo').click(function (e) {
   e.preventDefault();
   $('#input_file').click()
});
      $('#input_file').change(function () {
        if (this.files && this.files[0]) {
            if(this.files[0].size > (1048576 * 10)) {
                var agent = navigator.userAgent.toLowerCase();

                if ( (navigator.appName == 'Netscape' && navigator.userAgent.search('Trident') != -1) || (agent.indexOf("msie") != -1) ){
                    // ie 일때 input[type=file] init.
                    $('#input_file').replaceWith( $('#input_file').clone(true) );
                    } else {
                    //other browser 일때 input[type=file] init.
                    $('#input_file').val("");
                }
                alert('File size can\'t exceed 10m');
                return;
            }
          var reader = new FileReader();
          reader.onload = function (e) {
            $("#img_crop").attr("src", e.target.result);
            $("#modal_crop").modal("show");
          };
          reader.readAsDataURL(this.files[0]);
        }
      });

      /* SCRIPTS TO HANDLE THE CROPPER BOX */
    var image;
      var cropper
      $("#modal_crop").on("shown.bs.modal", function () {
          image = document.getElementById('img_crop');
          cropper = new Cropper(image, {
                viewMode: 2,
                minCropBoxWidth: 300,
                minCropBoxHeight: 300,
                aspectRatio: 1/1,
          });

      }).on("hidden.bs.modal", function () {
        cropper.destroy();
        var agent = navigator.userAgent.toLowerCase();

        if ( (navigator.appName == 'Netscape' && navigator.userAgent.search('Trident') != -1) || (agent.indexOf("msie") != -1) ){
            // ie 일때 input[type=file] init.
            $('#input_file').replaceWith( $('#input_file').clone(true) );
        } else {
            //other browser 일때 input[type=file] init.
                $('#input_file').val("");
        }
    });

      $(".js-zoom-in").click(function () {
        cropper.zoom(0.1);
      });

      $(".js-zoom-out").click(function () {
        cropper.zoom(-0.1);

      });

      /* SCRIPT TO COLLECT THE DATA AND POST TO THE SERVER
       * 모달 오픈시 너무 큰 그림이면 로딩하는 시간 주는 거 구현하고, 세이브 후 기다리는거 구현하고 체인지 안 되었어도 모달 꺼지면 디스트로이 하게 구현하라. */
      $(".js-crop-and-upload").click(function () {
        var cropData = cropper.getData();

        var form_file = $('#form_upload')[0];
        var form_data = new FormData(form_file);
        form_data.append('x', cropData["x"]);
        form_data.append('y', cropData["y"]);
        form_data.append('height', cropData["height"]);
        form_data.append('width', cropData["width"]);
        form_data.append('rotate', cropData["rotate"]);

        $.ajax({
            url:'/re_settings/ajax/upload_user_photo/',
            type:'post',
            dataType:'json',
            cache:false,
            processData: false,
            contentType: false,
            data:form_data,
            success:function (data) {
                $("#modal_crop").modal("hide");
                if (data.res === 1){
                    $('#img_300').attr('src', data.url)

                }
            }
        });
      });


    var val_name, val_username, val_email;

        $('#span_name').click(function (e) {
            e.preventDefault();
            val_name = $('#input_name').val();
            $.ajax({
                url:'/re_settings/ajax/',
                type:'post',
                dataType:'json',
                cache:false,
                data:{
                    command: 'name',
                    name: val_name,
                },
                success:function (data) {
                    if (data.res === 1){
                        $('#span_current_name').html(data.name);
                        $('#p_name_desc').html(data.message);
                        $('#input_name').val('');
                    } else if (data.res === 0){
                        $('#p_name_desc').html(data.message);
                    }
                }
            });
        })

        $('#span_username').click(function (e) {
            e.preventDefault();
            val_username = $('#input_username').val();
            $.ajax({
                url:'/re_settings/ajax/',
                type:'post',
                dataType:'json',
                cache:false,
                data:{
                    command: 'username',
                    username: val_username,
                },
                success:function (data) {
                    console.log(data)
                    if (data.res === 1){
                        $('#span_current_username').html(data.username);
                        $('#p_username_desc').html(data.message);
                        $('#input_username').val('');
                    } else if (data.res === 0){
                        $('#p_username_desc').html(data.message);
                    }
                }
            });
        });

        $(document).on('click', '#span_email', function (e) {
            e.preventDefault();
            var save_this = $(this);
            var middle_this = $('<span class="loader display_inline_block"></span>');
            $(this).replaceWith(middle_this)
            $.ajax({
                url:'/re_settings/ajax/',
                type:'post',
                dataType:'json',
                cache:false,
                data:{
                    command: 'email_resend',
                },
                success:function (data) {
                    if (data.res === 1){
                        $('#p_email_desc').html(data.email);
                        $('#input_email').val('');
                        middle_this.replaceWith(save_this)

                    } else if (data.res === 0){
                        $('#p_email_desc').html(data.message);
                    }
                }
            });

        })
        $(document).on('click', '#span_resend', function (e) {
            e.preventDefault();
            var save_this = $(this);
            var middle_this = $('<span class="loader display_inline_block"></span>');
            $(this).replaceWith(middle_this)
            $.ajax({
                url:'/re_settings/ajax/',
                type:'post',
                dataType:'json',
                cache:false,
                data:{
                    command: 'email_resend',
                },
                success:function (data) {
                    console.log(data)
                    if (data.res === 1){
                        $('#p_resend_desc').html(data.email);
                        middle_this.replaceWith(save_this)
                    } else if (data.res === 0){
                        $('#p_resend_desc').html(data.message);
                    }
                }
            });
        })
    })