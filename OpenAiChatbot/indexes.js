document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("form");
    const conversation = document.getElementById("chatbot-conversation");
    const exportBtn = document.getElementById("export-btn");
    const prevPageBtn = document.getElementById("prev-page");
    const nextPageBtn = document.getElementById("next-page");
    const searchInput = document.getElementById("search-input");
    const searchBtn = document.getElementById("search-btn");
    const clearChatBtn = document.getElementById("clear-chat-btn");
    const exportChatBtn = document.getElementById("export-chat-btn");

    let currentPage = 0;
    const pageSize = 5;

    // Open or create IndexedDB database
    const dbPromise = window.indexedDB.open("chatDB", 1);

    dbPromise.onupgradeneeded = function(event) {
        const db = event.target.result;
        if (!db.objectStoreNames.contains("messages")) {
            db.createObjectStore("messages", { keyPath: "id", autoIncrement: true });
        }
    };

    dbPromise.onsuccess = function(event) {
        console.log("IndexedDB opened successfully");
        displayMessagesFromDB();
    };

    form.addEventListener("submit", function(event) {
        event.preventDefault();
        const userInput = document.getElementById("user-input").value.trim();
        if (userInput !== "") {
            addMessage("user", userInput);
            // Add your logic to handle user input and generate bot response here
            // For now, let's simulate a bot response
            setTimeout(function() {
                addMessage("bot", "This is a bot response.");
            }, 1000);
            document.getElementById("user-input").value = ""; // Clear input field after sending message
            updateConversationHeight(); // Update conversation container height
        }
    });

    function addMessage(sender, message) {
        const messageContainer = document.createElement("div");
        messageContainer.classList.add("message", sender + "-message");

        const speechBubble = document.createElement("div");
        speechBubble.classList.add("speech-bubble");
        speechBubble.textContent = message;

        messageContainer.appendChild(speechBubble);
        conversation.appendChild(messageContainer); // Append message to the end
        conversation.scrollTop = conversation.scrollHeight; // Scroll to bottom
    }

    function updateConversationHeight() {
        const windowHeight = window.innerHeight;
        const containerTop = conversation.getBoundingClientRect().top;
        const containerBottom = windowHeight - containerTop;
        conversation.style.maxHeight = Math.min(containerBottom, windowHeight) - 20 + "px"; // Adjust padding
    }

    // JavaScript code
    document.addEventListener("DOMContentLoaded", function() {
        // Existing code...

        const refreshBtn = document.getElementById("refresh-btn");

        // Event listener for refresh button
        refreshBtn.addEventListener("click", function() {
            displayMessagesFromDB();
        });

        // Existing code...
    });

    // Update conversation height when the window is resized
    window.addEventListener("resize", updateConversationHeight);

    // Initial update of conversation height
    updateConversationHeight();

    // Export chat functionality
    exportBtn.addEventListener("click", function() {
        const messages = [];
        const messageElements = conversation.querySelectorAll(".message");
        messageElements.forEach(function(messageElement) {
            const sender = messageElement.classList.contains("user-message") ? "user" : "bot";
            const messageText = messageElement.querySelector(".speech-bubble").textContent;
            messages.push({ sender: sender, message: messageText });
        });

        // Convert messages array to JSON string
        const chatData = JSON.stringify(messages);
        console.log(chatData); // You can do whatever you want with this data, like saving it to a file or sending it to a server
    });

    prevPageBtn.addEventListener("click", function() {
        if (currentPage > 0) {
            currentPage--;
            displayMessagesFromDB();
        }
    });

    nextPageBtn.addEventListener("click", function() {
        currentPage++;
        displayMessagesFromDB();
    });

    searchBtn.addEventListener("click", function() {
        const searchTerm = searchInput.value.trim().toLowerCase();
        if (searchTerm !== "") {
            searchMessages(searchTerm);
        }
    });

    clearChatBtn.addEventListener("click", function() {
        clearChat();
    });

    exportChatBtn.addEventListener("click", function() {
        exportChat();
    });

    function displayMessagesFromDB() {
        const dbPromise = window.indexedDB.open("chatDB", 1);
        dbPromise.onsuccess = function(event) {
            const db = event.target.result;
            const transaction = db.transaction(["messages"], "readonly");
            const store = transaction.objectStore("messages");
            const request = store.getAll();
            request.onsuccess = function(event) {
                const messages = event.target.result;
                conversation.innerHTML = ""; // Clear conversation container
                const startIndex = currentPage * pageSize;
                const endIndex = startIndex + pageSize;
                for (let i = startIndex; i < endIndex && i < messages.length; i++) {
                    addMessage(messages[i].sender, messages[i].message, messages[i].timestamp);
                }
            };
        };
    }

    function searchMessages(searchTerm) {
        const dbPromise = window.indexedDB.open("chatDB", 1);
        dbPromise.onsuccess = function(event) {
            const db = event.target.result;
            const transaction = db.transaction(["messages"], "readonly");
            const store = transaction.objectStore("messages");
            const request = store.openCursor();
            request.onsuccess = function(event) {
                const cursor = event.target.result;
                if (cursor) {
                    const message = cursor.value;
                    if (message.message.toLowerCase().includes(searchTerm)) {
                        addMessage(message.sender, message.message, message.timestamp);
                    }
                    cursor.continue();
                }
            };
        };
    }

    function clearChat() {
        const dbPromise = window.indexedDB.open("chatDB", 1);
        dbPromise.onsuccess = function(event) {
            const db = event.target.result;
            const transaction = db.transaction(["messages"], "readwrite");
            const store = transaction.objectStore("messages");
            const request = store.clear();
            request.onsuccess = function(event) {
                currentPage = 0;
                displayMessagesFromDB();
                console.log("Chat history cleared");
            };
            request.onerror = function(event) {
                console.error("Error clearing chat history");
            };
        };
    }

    function exportChat() {
        const dbPromise = window.indexedDB.open("chatDB", 1);
        dbPromise.onsuccess = function(event) {
            const db = event.target.result;
            const transaction = db.transaction(["messages"], "readonly");
            const store = transaction.objectStore("messages");
            const request = store.getAll();
            request.onsuccess = function(event) {
                const messages = event.target.result;
                const chatData = JSON.stringify(messages);
                const blob = new Blob([chatData], { type: "application/json" });
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = "chat.json";
                document.body.appendChild(a);
                a.click();
                URL.revokeObjectURL(url);
            };
        };
    }
});
