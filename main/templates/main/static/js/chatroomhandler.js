var count = 0

const room_name = $("input[name='room_name']").val();
const username = $("input[name='username']").val();

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
    if (data.hasOwnProperty('au')) { 
        // au - add user

        $('.notification-section').append('<div class="notification">'
        + '<p class="notification-username"> <span class="notification-name">' + data.au + '</span> was added in the room</p>'
        + '<div class="notification-btns">'
        + '<button class="ok-btn">Ok</button>'
        + '<button class="remove-btn">Remove</button></div>'
        + '</div>');
    }

    else if (data.hasOwnProperty('add_user')) {

        var user = data.add_user
        console.log(data.add_user)

        $('.chat-room-members').append(
            '<li class="room-member"><p class="profile-pic">' + user.slice(0, 1).toUpperCase() 
            + '</p><div><p class="user-name">' + user + '</p><p class="time">joined 20mins ago</p>'
            + '<button class="remove-user">Remove</button></div></li>'
        );
    }

    else if (data.message) {

        time = get_current_time();

        $('.chat-logs').append('<div class="chat-msg"> '
            + '<p class="username"> ' + data.message[0] + '</p>'
            + '<p>' + data.message[1] + '</p>'
            + '<p class="time">' + time + '</p>'
        + '</div>');

        if (username === data.message[0]) {
            $('.chat-msg').css('left', '50%');
        }

        $('.chat-logs').scrollTop = $('.chat-logs').scrollHeight;
    }
}

$('.leave-room').click(['/'], remove_host); // closes socket connection and redirects host to home page
$('.logout-btn').click(['/user/logout/'], remove_host); // Logout the host and close the socket connection.
    
// removes host from the chat room and redirects to the requested url
function remove_host(redirect_url) {
    remove_user(username)
    client_socket.close();
    window.location.href = 'http://' + window.location.host + redirect_url;
}

$(document).on('click', '.ok-btn', (e) => {

    var current_notification_item = e.currentTarget.parentNode.parentNode;
    var username = current_notification_item.children[0].children[0].textContent;

    client_socket.send(JSON.stringify({
        'cu': username // confirm user
    }));

    current_notification_item.remove();
})

// host can remove the chat members
$(document).on('click', '.remove-btn', (e) => {
    var current_notification_item = e.currentTarget.parentNode.parentNode;

    var username = current_notification_item.children[0].children[0].textContent;
    remove_user(username);

    current_notification_item.remove();
})

$(document).on('click', '.room-member', (e) => {
    traget_elem = $(e)[0].currentTarget;

    traget_elem = $(traget_elem)[0].children[1].children[2];

    if ($(traget_elem).css('display') === 'none') {
        $(traget_elem).css('display', 'block');
    } else {
        $(traget_elem).css('display', 'none');
    }
});

$(document).on('click', '.remove-user', (e) => {
    traget_elem = $(e)[0].currentTarget;
    parent_elem = traget_elem.parentNode.parentNode;

    var username = $(parent_elem)[0].children[1].children[0].textContent;
    console.log(username);
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