function sendMessage() {
    const input = document.getElementById("input");
    const message = input.value;

    if (!message) return;

    const chatbox = document.getElementById("chatbox");

    // User message
    chatbox.innerHTML += `
        <div class="message user">${message}</div>
    `;

    fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: message})
    })
    .then(res => res.json())
    .then(data => {
        chatbox.innerHTML += `
            <div class="message bot">${data.response}</div>
        `;
        chatbox.scrollTop = chatbox.scrollHeight;
    });

    input.value = "";
}