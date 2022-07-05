const room_name = $("input[name='room_name']").val();
const username = $("input[name='username']").val();

var user_msg_count = 0

var is_host = false;

const client_socket = new WebSocket('ws://' + window.location.host + '/chat/room/' + room_name + '/')

// it will send username to the server, when a connection is made successfully.
client_socket.addEventListener('open', (e) => {

    client_socket.send(
        JSON.stringify({'username': username})
        );
})

client_socket.onmessage = (e) => {
    const data = JSON.parse(e.data);

    // it adds the user details in the notification panel,
    // chat room host only receive the notification from the server.

    if (data.hasOwnProperty('is_host')) {
        is_host = data.is_host;
    }

    else if (data.hasOwnProperty('notification')) { 
        // au - add user
        $('.notification-section').append(
            '<div class="dropdown-item rounded-bottom pb-1">'
			+ '<p class="newly-joined-member fw-medium pb-1">'+ data.notification +'</p>'
			+ '<div class="d-flex flex-row">'
			+ '<button class="btn btn-primary btn-sm ok-btn">OK</button>'
			+ '<button class="btn btn-outline-danger btn-sm remove-btn ms-2">Remove</button>'
			+ '</div>'
			+ '</div>'
        );
        $('.dropdown-toggle').css({"border-color": "red", 
                                    "border-width":"4px", 
                                    "border-style":"solid"
                                });
    }

    else if (data.hasOwnProperty('add_user')) {

        var user = data.add_user

        if (is_host) {
            $('.list-group').append(
                '<div class="list-group-item list-group-item-action pb-2 pt-3 d-flex flex-row justify-content-between">'
                + '<div class="user-pic d-flex flex-row">'
                + '<p class="pic rounded-circle text-center me-3 bg-success bg-gradient">' + user.slice(0, 2) + '</p>'
                + '<p class="room-members-name">' + user + '</p>'
                + '</div>'
                + '<button class="btn btn-danger remove-user fw-semibold  btn-sm">Remove</button>'
                + '</div>'
            );
        } else {
            $('.list-group').append(
                '<div class="list-group-item list-group-item-action pb-2 pt-3 d-flex flex-row justify-content-between">'
                + '<div class="user-pic d-flex flex-row">'
                + '<p class="pic rounded-circle text-center me-3 bg-success bg-gradient">' + user.slice(0, 2) + '</p>'
                + '<p class="room-members-name">' + user + '</p>'
                + '</div>'
                + '</div>'
            );
        }

    }

    else if (data.message) {

        var time = get_current_time();

        if (username === data.message[0]) {

            $('.chat-logs').append(
                '<div class="chat-msg-user'+ user_msg_count + ' chat-msg-user bg-primary ms-2">'
                + '<p class="messenger-name fw-semibold pe-3">' + data.message[0] + '</p>'
                + '<p class="msg text-white ps-2 pe-1">' + data.message[1] + '</p>'
                + '<p class="msg-time">' + time + '</p>'
                + '</div>'
            );

            var chat_screen_width = $('.chat-logs').width();
            var chat_item_width = $('.chat-msg-user'+user_msg_count).width();

            var left = (chat_screen_width - chat_item_width) -40;
            left = left + 'px';

            $('.chat-msg-user'+user_msg_count).css('left', left);
            user_msg_count++;

        } else {
            $('.chat-logs').append(
                '<div class="chat-msg bg-primary ms-2">'
                + '<p class="messenger-name fw-semibold pe-3">' + data.message[0] + '</p>'
                + '<p class="msg text-white ps-2 pe-1">' + data.message[1] + '</p>'
                + '<p class="msg-time">' + time + '</p>'
                + '</div>'
            );
        }

        $('.chat-logs').scrollTop = $('.chat-logs').scrollHeight;
    }

    else if (data.hasOwnProperty('remove_user')) {
        var _user = false

        for (var i=3; i < ($('.list-group')[0].children.length); i++) {

            var _child_elem = $('.list-group')[0].children[i];
            var _username = $('.list-group')[0].children[i].children[0].children[1].textContent;
            
            if (_username == data.remove_user) {
                _child_elem.remove();
                _user = true;
                break;
            } 
        }

        if (_user === false) {
            
            for (var i=0; i < ($('.notification-section')[0].children.length); i++) {

                var _child_elem = $('.notification-section')[0].children[i];
                var _username = _child_elem.children[0].textContent;
                
                if (_username === data.remove_user) {
                    _child_elem.remove();
                    _user = true;
                    break;
                }
            }
        }

        if ($('.notification-section')[0].children.length === 0) {
            $('.dropdown-toggle').css('border', '');
        }
    }
}

$('.leave-room').click(['/'], remove_client); // closes socket connection and redirects host to home page
$('.logout-btn').click(['/user/logout/'], remove_client); // Logout the host and close the socket connection.
    
// removes host from the chat room and redirects to the requested url
function remove_client(redirect_url) {
    remove_user(username)
    client_socket.close();
    window.location.href = 'http://' + window.location.host + redirect_url;
}

$(document).on('click', '.ok-btn', (e) => {
    
    var current_notification_item = e.currentTarget.parentNode.parentNode;
    var username = current_notification_item.children[0].textContent;

    client_socket.send(JSON.stringify({
        'req_to_au': username // confirm user
    }));

    current_notification_item.remove();

    if ($('.notification-section')[0].children.length === 0) {
        $('.dropdown-toggle').css('border', '');
    }
})

// host can remove the chat members
$(document).on('click', '.remove-btn', (e) => {

    var current_notification_item = e.currentTarget.parentNode.parentNode;
    var username = current_notification_item.children[0].textContent;
    remove_user(username);

    current_notification_item.remove();

    if ($('.notification-section')[0].children.length === 0) {
        $('.dropdown-toggle').css('border', '');
    }
})

$(document).on('click', '.remove-user', (e) => {
    traget_elem = $(e)[0].currentTarget;
    parent_elem = traget_elem.parentNode;
    var username = $(parent_elem)[0].children[0].children[1].textContent;

    parent_elem.remove();
    remove_user(username);
});

// send a request to remove user from the chat room
function remove_user(username) {
    client_socket.send(
        JSON.stringify({'ru': username})  //ru - remove user
    );
}

$('#chat-msg-input').keyup((e) => {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#submit-btn').click();
    }
});

// sends chat message to the server
$('#submit-btn').on('click', () => {
    const message = $('#chat-msg-input').val();
    
    client_socket.send(JSON.stringify({
        'message': [username, message]
    }));

    $('#chat-msg-input').val('');
})

function get_current_time() {

    const date = new Date();

    var h = date.getHours();
    var m = date.getMinutes();
    const am_pm = h >= 12? 'PM': 'AM';

    if (h > 12) {
        h = h%12;
    } else if (h === 0) {
        h = 12;
    }

    if (m < 10) {
        m = '0' + m;
    }

    return (h + ':' + m + ' ' + am_pm);
}

// websocket close event
client_socket.addEventListener('close', (e) => {
    window.location.href = 'http://' + window.location.host + '/';
});

window.addEventListener('beforeunload', function (e) {
    e.preventDefault();
    e.returnValue = '';
    remove_user(username);
});