const messagesDiv = document.getElementById("messages");
const userInput = document.getElementById("userInput");

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    // Show user message
    appendMessage("user", message);
    userInput.value = "";

    try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();
        appendMessage("bot", data.response);

    } catch (err) {
        console.error(err);
        appendMessage("bot", "Error: Cannot connect to the server.");
    }
}

// Append message to chat window
function appendMessage(sender, text) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender);
    messageDiv.textContent = text;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Allow pressing Enter key to send message
userInput.addEventListener("keydown", function(e) {
    if (e.key === "Enter") sendMessage();
});
