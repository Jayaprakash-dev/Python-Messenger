var count = 0

var room_name = $("input[name='room_name']").val();

const client_socket = new WebSocket('ws://' + window.location.host + '/chat/room/' + room_name + '/')

// it will send username to the server socket, when a connection is made successfully.
client_socket.addEventListener('open', (e) => {
    var username = $("input[name='username']").val();

    client_socket.send(
        JSON.stringify({'username': username})
        );
})

client_socket.onmessage = (e) => {
    const data = JSON.parse(e.data);
    console.log(data);
    console.log(data.hasOwnProperty('user'));

    if (data.user) {
        $('.username').html(data.user);
        $('.notification').css('display', 'block')
    }
}

$('.leave-room').on('click', () => {
    client_socket.close();
    window.location.href = 'http://' + window.location.host + '/';
})