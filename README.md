# AI Chatbot Web Application

## Features

- Welcome / login page
- Dynamic chat interface with real-time updates
- User message input + voice input support
- Dark mode and responsive design
- Session-based chat history
- Optional OpenAI API integration
- Clear history and logout controls

## Installation

pip install -r requirements.txt

## Optional AI API Integration

To use OpenAI instead of local fallback responses, set your API key:

```bash
set OPENAI_API_KEY=your_api_key_here
```

## Run

python app.py

Open Browser:

http://127.0.0.1:5000

## Notes

- The app uses a simple Flask login flow with session storage.
- Chat history is preserved during the session and can be cleared.
- Voice input works in browsers with Web Speech API support.
