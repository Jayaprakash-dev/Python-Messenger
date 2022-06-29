$("input[name='first_name']").keyup(checkNameFormat);
$("input[name='last_name']").keyup(checkNameFormat);

$("input[name='username']").keyup(checkNameFormat);

$("input[name='password1']").keyup(checkPassword);
$("input[name='password2']").keyup(checkPasswordMatching);

$(".pass-show-btn").on('click', showPassword);

function checkNameFormat(e) {
    e.preventDefault();

    var _username_input = $('input[name="username"]').val();
    var _first_name = $("input[name='first_name']").val();
    var _last_name = $("input[name='last_name']").val();
    var _csrf_token = $("input[type=hidden]").val();

    $.ajax({
        type: 'POST',
        url: '',
        data: {
                csrfmiddlewaretoken: _csrf_token,
                username: _username_input,
                first_name: _first_name,
                last_name: _last_name,
        },
        success: (data) => {
            if(data.message === '!name') {
                $('#name-status-icon').css('display', 'block');
                $('#name-status-msg').css('display', 'block');
                $('#username-section').css('margin-top', '0px');

                $('#username-status-icon').css('display', 'none');
                $('#username-status-msg').css('display', 'none');
                $('#password-section').css('margin-top', '15px');
            }
            else if(data.message === '!username') {
                $('#username-status-icon').css('display', 'block');
                $('#username-status-msg').css('display', 'block');
                $('#password-section').css('margin-top', '0px');

                $('#name-status-icon').css('display', 'none');
                $('#name-status-msg').css('display', 'none');
                $('#username-section').css('margin-top', '15px');
            } 
            else {
                $('#name-status-icon').css('display', 'none');
                $('#name-status-msg').css('display', 'none');
                $('#username-section').css('margin-top', '15px');

                $('#username-status-icon').css('display', 'none');
                $('#username-status-msg').css('display', 'none');
                $('#password-section').css('margin-top', '15px');
            }
        }
    });  
}

function checkPassword(e) {
    e.preventDefault();

    var _password_1 = $("input[name='password1']").val();
    var _csrf_token = $("input[type=hidden]").val();

    if(_password_1.length >= 8) {

        $('.least-msg').css('color', '#4BC502');
        $('#least-icon').attr('src', '/static/assets/Done.svg')

        $.ajax({
            type: 'POST',
            url: '',
            data: {
                csrfmiddlewaretoken: _csrf_token,
                password1: _password_1,
            },
            success: (data) => {
                if (data.message === 'pass_valid') {
                    $('.numeric-msg').css('color', '#4BC502');
                    $('#numeric-icon').attr('src', '/static/assets/Done.svg');
                    $('.alpha-msg').css('color', '#4BC502');
                    $('#alpha-icon').attr('src', '/static/assets/Done.svg');
                } else {
                    $('.numeric-msg').css('color', '#E24032');
                    $('#numeric-icon').attr('src', '/static/assets/wrong.svg');
                    $('.alpha-msg').css('color', '#E24032');
                    $('#alpha-icon').attr('src', '/static/assets/wrong.svg');
                }
            }
        });
    } else {
        $('.least-msg').css('color', '#E24032');
        $('#least-icon').attr('src', '/static/assets/wrong.svg')
        $('.numeric-msg').css('color', '#E24032');
        $('#numeric-icon').attr('src', '/static/assets/wrong.svg');
        $('.alpha-msg').css('color', '#E24032');
        $('#alpha-icon').attr('src', '/static/assets/wrong.svg');
    }
}

function checkPasswordMatching(e) {
    e.preventDefault();

    var _password_1 = $("input[name='password1']").val();
    var _password_2 = $("input[name='password2']").val();
    var _csrf_token = $("input[type=hidden]").val();

    if(_password_2.length >= 6) {
        $.ajax({
            type: 'POST',
            url: '',
            data: {
                    csrfmiddlewaretoken: _csrf_token, 
                    password1: _password_1,
                    password2: _password_2,
            },
            success: (data) => {
                if (data.message === 'pass_match') {
                    $('.password-match-msg').css('color', '#4BC502');
                    $('#match-icon').attr('src', '/static/assets/Done.svg')
            } else {
                    $('.password-match-msg').css('color', '#E24032');
                    $('#match-icon').attr('src', '/static/assets/wrong.svg')
                }
            }
        });
    }
}

function showPassword(e) {
    e.preventDefault;

    var pass_status = $('#password').attr('type');

    if (pass_status === 'password') {
        $('#password').attr('type', 'text');
    } else {
        $('#password').attr('type', 'password');
    }
}