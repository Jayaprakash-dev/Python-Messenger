$('input').keyup(checkForm);

function checkForm(e) {
    e.preventDefault();

    var _username_input = $('input[type=text]').val();
    var _email_input = $('input[type=email]').val();
    var _csrf_token = $("input[type=hidden]").val();

    $.ajax({
        type: 'POST',
        url: '',
        data: {'csrfmiddlewaretoken': _csrf_token, 
                'username': _username_input, 
                'email': _email_input
            },
        success: function(data) {
            if (data.message === undefined) {
                $('.message').empty();
            }
            else {
                $('.message').html(data.message);
            }
        },
    });
}

