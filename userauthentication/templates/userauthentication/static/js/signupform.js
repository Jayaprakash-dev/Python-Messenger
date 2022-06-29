$("input[type=password]").attr('placeholder', 'must be 8 characters');
$("input[name='password2']").keyup(checkForm);
$("input[name='first_name']").keyup(checkForm);
$("input[name='last_name']").keyup(checkForm);

function checkForm(e) {
    e.preventDefault();

    var _username_input = $('input[name="username"]').val();
    var _email_input = $('input[type=email]').val();
    var _first_name = $("input[name='first_name']").val();
    var _last_name = $("input[name='last_name']").val();
    var _password_1 = $("input[name='password1']").val();
    var _password_2 = $("input[name='password2']").val();
    var _csrf_token = $("input[type=hidden]").val();

    if(_password_2.length >= 3) {
        $.ajax({
            type: 'POST',
            url: '',
            data: {
                    csrfmiddlewaretoken: _csrf_token, 
                    username: _username_input,
                    email: _email_input,
                    first_name: _first_name,
                    last_name: _last_name, 
                    password1: _password_1,
                    password2: _password_2,
            },
            success: (data) => {
                if (data.message === undefined) {
                    $('.message').empty();
                }
                else {
                    $('.message').html(data.message);
                }
            }
        });
    } else {
        $.ajax({
            type: 'POST',
            url: '',
            data: {
                    csrfmiddlewaretoken: _csrf_token,
                    first_name: _first_name,
                    last_name: _last_name, 
                    password1: 0,
                    password2: 1,
            },
            success: (data) => {
                if (data.message === undefined) {
                    $('.message').empty();
                }
                else {
                    $('.message').html(data.message);
                }
            }
        });
    }
}