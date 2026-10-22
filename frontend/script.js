
const API_URL = "http://127.0.0.1:8000/chat";

const chat = document.getElementById("chat");
const form = document.getElementById("chat-form");
const input = document.getElementById("question");
const sendButton = document.getElementById("send");
const errorBox = document.getElementById("error");

function addMessage(text, type, sourceUrl = null) {
    const message = document.createElement("div");
    message.className = `message ${type}`;
    message.textContent = text;

    if (sourceUrl && type === "bot") {
        try {
            const url = new URL(sourceUrl);

            if (url.protocol === "https:" &&
                url.hostname === "www.gvpcew.ac.in") {
                const link = document.createElement("a");
                link.className = "source";
                link.href = url.href;
                link.target = "_blank";
                link.rel = "noopener noreferrer";
                link.textContent = "View official source ↗";

                message.appendChild(document.createElement("br"));
                message.appendChild(link);
            }
        } catch {
            // Ignore an invalid source URL.
        }
    }

    chat.appendChild(message);
    chat.scrollTop = chat.scrollHeight;
}

async function sendQuestion(question) {
    question = question.trim();

    if (!question || sendButton.disabled) return;

    errorBox.hidden = true;
    addMessage(question, "user");

    input.value = "";
    input.disabled = true;
    sendButton.disabled = true;
    sendButton.textContent = "Wait...";

    const loading = document.createElement("div");
    loading.className = "message bot";
    loading.textContent = "Finding the best answer...";
    chat.appendChild(loading);
    chat.scrollTop = chat.scrollHeight;

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question })
        });

        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }

        const data = await response.json();
        loading.remove();

        addMessage(
            data.answer || "No answer was returned.",
            "bot",
            data.source_url
        );

    } catch (error) {
        loading.remove();
        errorBox.textContent =
            "Could not connect to the chatbot. Check that the backend server is running.";
        errorBox.hidden = false;

    } finally {
        input.disabled = false;
        sendButton.disabled = false;
        sendButton.textContent = "Send ➤";
        input.focus();
    }
}

form.addEventListener("submit", function(event) {
    event.preventDefault();
    sendQuestion(input.value);
});

document.querySelectorAll(".suggestion").forEach(button => {
    button.addEventListener("click", function() {
        sendQuestion(button.textContent);
    });
});
