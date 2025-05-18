# 🇻🇳 Vietnamese Cooking Chatbot

A smart Vietnamese culinary chatbot that helps you:
- Suggest dishes based on available ingredients  
- Provide step-by-step cooking instructions  
- Recommend ingredient substitutions  
- Advise based on dietary preferences  
- Calculate appropriate serving sizes  

## 🧠 How It Works

This chatbot is built with Retrieval-Augmented Generation (RAG), combining:
- A local LLM model (`phogpt-4b-chat-gguf`) for reasoning and language generation
- A recipe retrieval system indexing around **2,400 Vietnamese cooking recipes** for accurate responses

The system first searches relevant cooking instructions, then feeds those into the model to generate contextualized answers.

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/your-username/vietnamese-cooking-chatbot.git
cd vietnamese-cooking-chatbot
```
### 2. Download the .gguf model file
Download the [PhoGPT-4B-Chat GGUF](https://huggingface.co/vinai/PhoGPT-4B-Chat-gguf/tree/main) model
and place it in the model/ directory (create the folder if it doesn’t exist).
Example path after downloading:
```
vietnamese-cooking-chatbot/
└── model/
    └── PhoGPT-4B-Chat.gguf
```
### 3. Modify the model path in app.py
Make sure this line is set correctly in src/app.py:
```
llm = get_llm('model/PhoGPT-4B-Chat.gguf') # or your own path
```
### 4. Install required dependencies
```
pip install -r requirements.txt
``` 
### 5. Run the FastAPI server with Uvicorn
```
uvicorn src.app:app --host "0.0.0.0" --port 5001 --reload
```

Once the server is running, you can interact with the chatbot using either of the following methods:

1. POST Request (Single Response):
   - Endpoint: POST http://localhost:5001/chatbot
   - Request Body (JSON): {"id": "<thread_id>", "question": "<your question>"}
   - The server will return a single response from the chatbot.

2. WebSocket Streaming (Real-time Response):
   - Connect to: ws://localhost:5001/ws/<thread_id>
   - Send text messages through the WebSocket
   - Receive the chatbot's responses as a stream (step by step)

You can also access a demo HTML chat interface at:
   - http://localhost:5001/
