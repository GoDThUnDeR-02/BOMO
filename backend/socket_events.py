from flask_socketio import emit, join_room

def register_socket_events(socketio):

    @socketio.on("join_room")
    def join(data):
        join_room(data["room"])

    @socketio.on("send_message")
    def handle_message(data):
        emit("receive_message", data, room=data["room"])
