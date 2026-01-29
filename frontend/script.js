const socket = io("http://localhost:5000");
const room = "user1_user2";

socket.emit("join_room", { room });

function send() {
  const msg = document.getElementById("msg").value;

  socket.emit("send_message", {
    room: room,
    message: msg,
    sender: "user1"
  });
}

socket.on("receive_message", data => {
  const chat = document.getElementById("chat");
  chat.innerHTML += `<p>${data.sender}: ${data.message}</p>`;
});
