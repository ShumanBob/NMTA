
document.addEventListener("DOMContentLoaded", function () {
  const chatMessages = document.getElementById("chat-messages");
  const chatInput = document.getElementById("chat-input");
  const sendBtn = document.getElementById("send-btn");

  async function sendMessage() {
    const message = chatInput.value.trim();
    if (message === "") return;

    // show user message
    const userDiv = document.createElement("div");
    userDiv.innerHTML = `<strong>You:</strong> ${message}`;
    chatMessages.appendChild(userDiv);

    // clear input
    chatInput.value = "";

    // thinking animation
    const botDiv = document.createElement("div");
    botDiv.innerHTML = `<strong>TA:</strong> <span id="typing">Thinking...</span>`;
    chatMessages.appendChild(botDiv);

    try {
      const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message }),
      });

      const data = await response.json();

      // replace bot message
      botDiv.innerHTML = `<strong>TA:</strong> ${data.response}`;
    } catch (error) {
      botDiv.innerHTML = `<strong>TA:</strong> Sorry, an error occurred.`;
      console.error("Chat error:", error);
    }

    chatMessages.scrollTop = chatMessages.scrollHeight;
  }


  sendBtn.addEventListener("click", sendMessage);
  chatInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") sendMessage();
  });
});