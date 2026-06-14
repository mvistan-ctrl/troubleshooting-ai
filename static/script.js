document.getElementById("sendBtn").addEventListener("click", sendMessage);
document.getElementById("message").addEventListener("keypress", function(e) {
    if (e.key === "Enter") sendMessage();
});

document.getElementById("themeToggle").addEventListener("click", () => {
    document.body.classList.toggle("dark");
});

//async function sendMessage() {
    async function sendMessage() {
    const message = document.getElementById("message").value;
    const token = localStorage.getItem("token");

    const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({ message })
    });

    const data = await response.json();

    // FIX IS HERE
    const aiReply = data.reply;
    console.log("API returned:", data);
    addMessage("user", message);
    addMessage("ai", aiReply);
    //localStorage.getItem("token");

}

function addMessage(sender, text) {
    const chatBox = document.getElementById("chat-box");

    const bubble = document.createElement("div");
    bubble.classList.add("bubble");

    if (sender === "user") {
        bubble.classList.add("user-bubble");
    } else {
        bubble.classList.add("ai-bubble");
    }

//    bubble.textContent = text;
    bubble.innerHTML = marked.parse(text);  
    chatBox.appendChild(bubble);

    chatBox.scrollTop = chatBox.scrollHeight;
}


    
    //const input = document.getElementById("message");
    //const chatbox = document.getElementById("chatbox");
    //const typing = document.getElementById("typing");

    //const userText = input.value.trim();
    //if (!userText) return;

    // Add user message
    //chatbox.innerHTML += `<div class="msg user">${userText}</div>`;
    //input.value = "";
  //  chatbox.scrollTop = chatbox.scrollHeight;

    // Show typing indicator
    //typing.classList.remove("hidden");

    // Send to backend
    //const response = await fetch("/api/chat", {
      //  method: "POST",
        //headers: { "Content-Type": "application/json" },
        //body: JSON.stringify({ message: userText })
    //});

    //const data = await response.json();

    // Hide typing indicator
   // typing.classList.add("hidden");

    // Add AI message
    //chatbox.innerHTML += `<div class="msg bot">${data.reply}</div>`;
    //chatbox.scrollTop = chatbox.scrollHeight;
//}
