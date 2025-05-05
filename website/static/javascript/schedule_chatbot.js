// opens chatbot
function openChatbot() {
    const container = document.getElementById("chatbot-popup");
    container.style.display = "block";
    initChatbot();
}
// close chatbot popup
function closeChatbot() {
    document.getElementById("chatbot-popup").style.display = "none";
}
// intitalizes chatbot functionality; event listeners and message handling
function initChatbot() {
    const chatMessages = document.getElementById("chatbot-messages");
    const chatInput = document.getElementById("chatbot-input");
    const sendBtn = document.getElementById("chatbot-send-btn");

    // prevent intialization if already
    if (!sendBtn || sendBtn.dataset.initialized) return;
    sendBtn.dataset.initialized = "true";
    // sends message to server and displays response
    async function sendMessage() {
        const message = chatInput.value.trim();
        if (message === "") return;
        // display user message
        const userDiv = document.createElement("div");
        userDiv.innerHTML = `<strong>You:</strong> ${message}`;
        chatMessages.appendChild(userDiv);
        chatInput.value = "";
        // show placeholder message while waiting for server response
        const botDiv = document.createElement("div");
        botDiv.innerHTML = `<strong>TA:</strong> <span id="typing">Thinking...</span>`;
        chatMessages.appendChild(botDiv);
        // send the user message to the server
        try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
        });
        // parse server response and update message
        const data = await response.json();
        botDiv.innerHTML = `<strong>TA:</strong> ${data.response}`;
        } catch (error) {
        botDiv.innerHTML = `<strong>TA:</strong> Sorry, an error occurred.`;
        console.error("Chat error:", error);
        }
        // sscroll chat to latest message
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    // trigger sendMessage when button is used
    sendBtn.addEventListener("click", sendMessage);
    // trigger sendMessage when enter key is pressed
    chatInput.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
        e.preventDefault();
        sendMessage();
        }
    });
}