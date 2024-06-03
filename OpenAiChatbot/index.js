import { Configuration, OpenAIApi } from 'openai';

// Set up OpenAI configuration with API key
const configuration = new Configuration({
    apiKey: process.env.OPENAI_API_KEY
});

// Initialize OpenAI API
const openai = new OpenAIApi(configuration);

// Array to store conversation
const conversationArr = [
    { 
        role: 'system',
        content: 'You are a useful assistant.' // Instruction for chatbot
    }
];

// Function to render user's message
function renderUserMessage(text) {
    const chatbotConversation = document.getElementById('chatbot-conversation');
    const newSpeechBubble = document.createElement('div');
    newSpeechBubble.classList.add('speech', 'speech-human');
    chatbotConversation.appendChild(newSpeechBubble);
    newSpeechBubble.textContent = text;
    conversationArr.push({ role: 'user', content: text }); // Update conversation array
}

// Function to fetch AI response
async function fetchReply() {
    const userInput = document.getElementById('user-input').value;
    renderUserMessage(userInput); // Render user's message to DOM
    document.getElementById('user-input').value = ''; // Clear input field
    const response = await openai.createChatCompletion({
        model: 'gpt-4',
        messages: conversationArr
    });
    const aiResponse = response.data.choices[0].message.content;
    renderTypewriterText(aiResponse); // Render AI's response with typewriter effect
    conversationArr.push(response.data.choices[0].message); // Update conversation array
}

// Function to render AI's response with typewriter effect
function renderTypewriterText(text) {
    const chatbotConversation = document.getElementById('chatbot-conversation');
    const newSpeechBubble = document.createElement('div');
    newSpeechBubble.classList.add('speech', 'speech-ai', 'blinking-cursor');
    chatbotConversation.appendChild(newSpeechBubble);
    
    let i = 0;
    const interval = setInterval(() => {
        newSpeechBubble.textContent += text.slice(i - 1, i);
        if (text.length === i) {
            clearInterval(interval);
            newSpeechBubble.classList.remove('blinking-cursor');
        }
        i++;
        chatbotConversation.scrollTop = chatbotConversation.scrollHeight;
    }, 50);
}

// Event listener for form submission
document.getElementById('form').addEventListener('submit', (e) => {
    e.preventDefault();
    fetchReply(); // Fetch AI's response when user submits form
});
