var count = 0

const room_name = $("input[name='room_name']").val();
const username = $("input[name='username']").val();

const client_socket = new WebSocket('ws://' + window.location.host + '/chat/room/' + room_name + '/')

// it will send username to the server socket, when a connection is made successfully.
client_socket.addEventListener('open', (e) => {

    client_socket.send(
        JSON.stringify({'username': username})
        );
})

client_socket.onmessage = (e) => {
    const data = JSON.parse(e.data);
    console.log(data);
    console.log(data.hasOwnProperty('user'));

    if (data.user) {
        $('.notification').css('display', 'block');
        $('.notification-username').html(data.user);
    }
}

$('.leave-room').on('click', closeRoom);
$('.logout-btn').on('click', logout_user);
    

function closeRoom() {
    client_socket.send(
        JSON.stringify({'ru': username})
        );
    client_socket.close();
    window.location.href = 'http://' + window.location.host + '/';
}

function logout_user() {
    client_socket.close();
    window.location.href = 'http://' + window.location.host + '/user/logout/';
}

$('.ok-btn').on('click', () => {

    var username = $('.notification-username')[0].textContent;

    $('.chat-room-members').append(
        '<li><img src="" alt="P" class="profile-pic"><div><p class="user-name">' + username + '</p><p class="time">joined 20mins ago</p></div></li>'
    );

    $('.notification').css('display', 'none');
})