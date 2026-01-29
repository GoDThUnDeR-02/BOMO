const room = "user1_user2";
const ws = new WebSocket(`ws://localhost:8000/ws/${room}`);

ws.onmessage = (event) => {
  document.getElementById("chat").innerHTML += `<p>${event.data}</p>`;
};

function send() {
  const msg = document.getElementById("msg").value;
  ws.send(msg);
}
