var count = 0

var room_name = $("input[name='room_name']").val();

const client_socket = new WebSocket('ws://' + window.location.host + '/chat/room/' + room_name + '/')

client_socket.onmessage = (e) => {
    console.log(e);
    const data = JSON.parse(e.data);

    if (data.message === 'member added') {
        
    }
    $('.chat-logs').html(data.message)
}

// it will send username to the server socket, when a connection is made successfully.
client_socket.addEventListener('open', (e) => {
    var username = $("input[name='username']").val();

    client_socket.send(
        JSON.stringify({'username': username})
        );
})

$('.leave-room').on('click', () => {
    client_socket.close();
    window.location.href = 'http://' + window.location.host + '/';
})