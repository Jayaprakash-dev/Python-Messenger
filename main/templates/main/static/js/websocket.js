function submitForm() {

    const room_id = JSON.parse(document.getElementById('room-id').value);
    console.log(room_id);

    const client_socket = new WebSocket('ws://' + window.location.host + '/chat/room/' + room_id + '/');

    client_socket.onclose(() => {
        alert("Socket connection closed...");
    });
}