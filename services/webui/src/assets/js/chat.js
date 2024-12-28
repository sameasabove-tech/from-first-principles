document.addEventListener("DOMContentLoaded", () => {
    const chatMessages = document.getElementById("chat-messages");
    const chatInput = document.getElementById("chat-input");
    const sendBtn = document.getElementById("send-btn");
    const llmModelSelect = document.getElementById("llm-model"); 
  
    const addMessage = (text, sender) => {
        const messageDiv = document.createElement("div");
        messageDiv.className = `message ${sender}`;
  
        if (sender === "bot") {
            const img = document.createElement('img');
            img.src = '../assets/images/tab-logo.png'; 
            img.alt = 'Bot Logo';
            messageDiv.appendChild(img);
  
  
        }
  
        messageDiv.append(text); 
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight; 
    };
  
  
    const sendMessage = async () => {
        const userMessage = chatInput.value.trim();
        if (!userMessage) return;
  
        addMessage(userMessage, "user");
        chatInput.value = "";
  
        const selectedModel = llmModelSelect.value;
  
        try {
            const response = await fetch("http://127.0.0.1:8080/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userMessage, model: selectedModel }),
            });
            const data = await response.json();
            addMessage(data.response, "bot");
        } catch (error) {
            console.error("Error:", error);
            addMessage("Error connecting to server.", "bot");
        }
    };
  
    sendBtn.addEventListener("click", sendMessage);
  
    chatInput.addEventListener("keyup", (event) => {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
  });
  
  