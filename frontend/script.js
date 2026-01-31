const chat = document.getElementById("chat");

const BASE_URL = "https://YOUR-RENDER-APP.onrender.com";

// 1️⃣ Open SSE connection
const eventSource = new EventSource(`${BASE_URL}/events`);

eventSource.onmessage = (event) => {
  if (!event.data || event.data === "{}") return;

  const msg = JSON.parse(event.data);
  chat.innerHTML += `<p>${msg.text}</p>`;
  chat.scrollTop = chat.scrollHeight;
};

eventSource.onerror = () => {
  console.log("SSE connection lost, retrying...");
};

// 2️⃣ Send message via HTTP POST
function send() {
  const input = document.getElementById("msg");
  const text = input.value.trim();
  if (!text) return;

  fetch(`${BASE_URL}/send`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });

  input.value = "";
}
