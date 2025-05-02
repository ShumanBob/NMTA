function openChatbot() {
    const container = document.getElementById("chatbot-popup");
    container.style.display = "block";
    initChatbot();
}

function closeChatbot() {
    document.getElementById("chatbot-popup").style.display = "none";
}

function initChatbot() {
    const chatMessages = document.getElementById("chatbot-messages");
    const chatInput = document.getElementById("chatbot-input");
    const sendBtn = document.getElementById("chatbot-send-btn");

    if (!sendBtn || sendBtn.dataset.initialized) return;
    sendBtn.dataset.initialized = "true";

    async function sendMessage() {
        const message = chatInput.value.trim();
        if (message === "") return;

        const userDiv = document.createElement("div");
        userDiv.innerHTML = `<strong>You:</strong> ${message}`;
        chatMessages.appendChild(userDiv);
        chatInput.value = "";

        const botDiv = document.createElement("div");
        botDiv.innerHTML = `<strong>TA:</strong> <span id="typing">Thinking...</span>`;
        chatMessages.appendChild(botDiv);

        try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
        });

        const data = await response.json();
        botDiv.innerHTML = `<strong>TA:</strong> ${data.response}`;
        } catch (error) {
        botDiv.innerHTML = `<strong>TA:</strong> Sorry, an error occurred.`;
        console.error("Chat error:", error);
        }

        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    sendBtn.addEventListener("click", sendMessage);
    chatInput.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
        e.preventDefault();
        sendMessage();
        }
    });
}