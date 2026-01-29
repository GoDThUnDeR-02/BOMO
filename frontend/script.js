const room = "user1_user2";
const ws = new WebSocket(
  "wss://your-render-app-name.onrender.com/ws/user1_user2"
);


ws.onmessage = (event) => {
  document.getElementById("chat").innerHTML += `<p>${event.data}</p>`;
};

function send() {
  const msg = document.getElementById("msg").value;
  ws.send(msg);
}
