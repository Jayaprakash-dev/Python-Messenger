$("input[name='password2']").keyup(checkPassword);

function checkPassword(e) {
    e.preventDefault();

    var _password_1 = $("input[name='password1']").val()
    var _password_2 = $("input[name='password2']").val()
    var _csrf_token = $("input[type=hidden]").val();

    if(_password_2.length >= 8) {
        $.ajax({
            type: 'POST',
            url: '',
            data: {'csrfmiddlewaretoken': _csrf_token, 
                    'password1': _password_1,
                    'password2': _password_2
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