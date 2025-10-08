# Smart-chat-assitant
Smart Chat Assistant
A simple Streamlit chat app using Google Gemini, with multi‑session history, search, and export.

Features
Multiple chat sessions with titles and timestamps.

Gemini model fallback: gemini‑2.0‑flash‑exp → 1.5‑flash → 1.5‑pro.

Search chats and export current chat (TXT) or all chats (JSON).

Clear current chat and archive old chats.

Setup
Python 3.9+ recommended.

Install: pip install streamlit google-generativeai.

Set API key securely (do not hardcode):

macOS/Linux: export GEMINI_API_KEY="YOUR_KEY"

Windows (PowerShell): setx GEMINI_API_KEY "YOUR_KEY"

Run
streamlit run app.py.

Notes
The code currently shows a placeholder API key constant; switch to env vars or Streamlit secrets before publishing.

If no compatible model is found, the app shows an API error.
