Smart Chat Assistant 💬
A multi-session chat application built with Streamlit and the Google Gemini API. It lets you manage multiple conversations, search history, and export your data.

Key Features:
Multi-Session History: Keep and switch between different chat conversations.

Search: Easily search old chats by title or message content.

Data Export: Download conversations as Text or JSON files.

Chat Management: Start new chats and clear/archive old ones.

Getting Started
1. Requirements
You need Python 3.8+.

2. Setup
Install the required libraries:

Bash

pip install streamlit google-genai
3. API Key
You must replace the placeholder API key in your app.py file with your actual Gemini API Key.

Python

# In app.py: Replace this with your key
GEMINI_API_KEY = "YOUR_ACTUAL_API_KEY_HERE"
4. Run the App
Start the application from your terminal:

Bash

streamlit run app.py
Usage
Chat: Type your message and press Enter.

New Chat: Click 💬 New chat in the sidebar.

Switch Chats: Click on any conversation title listed under Chats in the sidebar.

Export Data: Use the Export Options buttons to save your current chat or all chat history.
