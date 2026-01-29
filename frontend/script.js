const room = "user1_user2";

const ws = new WebSocket(
  "wss://bumo-klfa.onrender.com/ws/user1_user2"
);

ws.onopen = () => {
  console.log("Connected to BUMO WebSocket");
};

ws.onmessage = (event) => {
  const chat = document.getElementById("chat");
  chat.innerHTML += `<p>${event.data}</p>`;
};

ws.onerror = (err) => {
  console.error("WebSocket error:", err);
};

function send() {
  const msg = document.getElementById("msg").value;
  ws.send(msg);
}
