var validate_base = (function validate_base() {

        var banned_username_list = ['avastove'];
        var banned_password_list = [
            'password', 'qwerty', 'superman', '123456', '1234567', '12345678', '123456789', '1234567890', '012345', '0123456',
            '01234567', '012345678', '0123456789', '111111', 'aaaaaa'
        ];

        var name = $('#id_name').val();
        var username = $('#id_username').val();
        var email = $('#id_email').val();
        var password = $('#id_password').val();
        var password_confirm = $('#id_password_confirm').val();

        if (typeof password === 'undefined'){
            var username_validator=username_validate(username, banned_username_list);
            if (username_validator===0){
                $('#p_clue').html('It\'s unavailable username');
                return false;
            }
            if (!(6 <= username.length && username.length <= 30)){
                $('#p_clue').html('username should be 6 <= username <= 30 greater than or equal to 6, less than or equal to 30');
                return false;
            }
            if (8 <= username.length && /^\d+$/.test(username)){
                $('#p_clue').html('If username length is greater than or equal to 8, cannot be made of only digits');
                return false;

            }
            if (!(/^([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)$/.test(username))){
                $('#p_clue').html('username can be made of digit, alphabet, . or _');
                return false;

            }
            if (!(1 <= name.length && name.length <= 30)){
                $('#p_clue').html('name should be 1 <= name <= 30 greater than or equal to 6, less than or equal to 30');
                return false;

            }
            if (!(/[^@]+@[^@]+\.[^@]+/.test(email))){
                $('#p_clue').html('It\'s unavailable email');
                return false;
            }
            if (255 < email.length){
                $('#p_clue').html('You have to change email length');
                return false;

            }

        }
        else {
            var username_validator=username_validate(username, banned_username_list);
            if (username_validator===0){
                $('#p_clue').html('It\'s unavailable username');
                return false;
            }
            if (!(6 <= username.length && username.length <= 30)){
                $('#p_clue').html('username should be 6 <= username <= 30 greater than or equal to 6, less than or equal to 30');
                return false;
            }
            if (8 <= username.length && /^\d+$/.test(username)){
                $('#p_clue').html('If username length is greater than or equal to 8, cannot be made of only digits');
                return false;

            }
            if (!(/^([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)$/.test(username))){
                $('#p_clue').html('username can be made of digit, alphabet, . or _');
                return false;

            }
            if (!(1 <= name.length && name.length <= 30)){
                $('#p_clue').html('name should be 1 <= name <= 30 greater than or equal to 6, less than or equal to 30');
                return false;

            }
            if (!(/[^@]+@[^@]+\.[^@]+/.test(email))){
                $('#p_clue').html('It\'s unavailable email');
                return false;

            }
            if (255 < email.length){
                $('#p_clue').html('You have to change email length');
                return false;

            }
            if (password !== password_confirm) {
                $('#p_clue').html('both passwords you submitted are not the same');
                return false;

            }
            if (!(6 <= password.length && password.length <= 128)){
                $('#p_clue').html('password should be 6 <= password <= 128 greater than or equal to 6, less than or equal to 128');
                return false;

            }
            if (username === password){
                $('#p_clue').html('password cannot be the same as username');
                return false;

            }
            if ($.inArray(password, banned_password_list)!==-1){
                $('#p_clue').html('It\'s unavailable password');
                return false;
            }
            if ($('#years option:selected').val() === 'non' ||$('#months option:selected').val() === 'non' ||$('#days option:selected').val() === 'non'){
                $('#p_clue').html('It\'s unavailable Birthday');
                return false;
            }

        }
        return true;
    });

    function username_validate(needle, haystack) {
        var length = haystack.length;
        for (var i = 0; i < length; i++) {
            var result = needle.indexOf(haystack[i])!==-1;
            if (result===true){
                return 0;
            }
        }
        return 1;
    }