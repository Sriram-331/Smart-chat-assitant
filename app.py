import streamlit as st
import google.generativeai as genai
from datetime import datetime
import json

# Configure page
st.set_page_config(
    page_title="Smart Chat Assistant",
    page_icon="💬",
    layout="wide"
)

# Hardcoded API key - Replace with your actual API key
GEMINI_API_KEY = "AIzaSyCinHudyssFmnMioekBWYu4woWYvFux8Ww"

# Configure Gemini
model = None
api_error = None

try:
    genai.configure(api_key=GEMINI_API_KEY)
    # Use Gemini 2.0 Flash model as requested
    model_names = ['gemini-2.0-flash-exp', 'gemini-1.5-flash', 'gemini-1.5-pro']
    
    for model_name in model_names:
        try:
            model = genai.GenerativeModel(model_name)
            # Test the model with a simple request
            test_response = model.generate_content("Hello")
            break
        except Exception as model_error:
            continue
    
    if model is None:
        api_error = "No compatible AI model found"
        
except Exception as e:
    api_error = str(e)

# Initialize session state for chat history
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {}
if "current_session_id" not in st.session_state:
    session_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    st.session_state.current_session_id = session_id
    st.session_state.chat_sessions[session_id] = {
        "messages": [],
        "title": "New Chat",
        "created_at": datetime.now()
    }

# Custom CSS for dark theme sidebar
st.markdown("""
<style>
    .sidebar-content {
        background-color: #1e1e1e;
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .sidebar-button {
        background-color: #2d2d2d;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        margin: 0.25rem 0;
        border-radius: 6px;
        width: 100%;
        text-align: left;
        cursor: pointer;
    }
    .sidebar-button:hover {
        background-color: #3d3d3d;
    }
    .section-header {
        color: #888;
        font-size: 0.9rem;
        margin: 1rem 0 0.5rem 0;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with enhanced options
with st.sidebar:
    st.title("💬 Smart Chat")
    
    # Main Actions Section
    st.markdown('<div class="section-header">Main Actions</div>', unsafe_allow_html=True)
    
    # New Chat button
    if st.button("💬 New chat", use_container_width=True, key="new_chat"):
        session_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        st.session_state.current_session_id = session_id
        st.session_state.chat_sessions[session_id] = {
            "messages": [],
            "title": "New Chat",
            "created_at": datetime.now()
        }
        st.rerun()
    
    # Search chats
    search_query = st.text_input("🔍 Search chats", placeholder="Search your conversations...", key="search_chats")
    
    # Export Options Section
    st.markdown('<div class="section-header">Export Options</div>', unsafe_allow_html=True)
    
    if st.button("📄 Export Current Chat", use_container_width=True):
        current_session = st.session_state.chat_sessions[st.session_state.current_session_id]
        if current_session["messages"]:
            # Create export content
            export_content = f"# {current_session['title']}\n\n"
            export_content += f"**Created:** {current_session['created_at'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            for msg in current_session["messages"]:
                role = "**You:**" if msg["role"] == "user" else "**Assistant:**"
                export_content += f"{role} {msg['content']}\n\n"
            
            st.download_button(
                label="💾 Download as Text",
                data=export_content,
                file_name=f"{current_session['title'][:20]}.txt",
                mime="text/plain"
            )
    
    if st.button("📊 Export All Chats", use_container_width=True):
        if st.session_state.chat_sessions:
            # Export all sessions as JSON
            export_data = {}
            for session_id, session_data in st.session_state.chat_sessions.items():
                export_data[session_id] = {
                    "title": session_data["title"],
                    "created_at": session_data["created_at"].isoformat(),
                    "messages": session_data["messages"]
                }
            
            st.download_button(
                label="💾 Download All as JSON",
                data=json.dumps(export_data, indent=2),
                file_name=f"chat_history_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
    
    # Chat Management Section
    st.markdown('<div class="section-header">Chat Management</div>', unsafe_allow_html=True)
    
    if st.button("🗑️ Clear Current Chat", use_container_width=True):
        current_session = st.session_state.chat_sessions[st.session_state.current_session_id]
        current_session["messages"] = []
        current_session["title"] = "New Chat"
        st.rerun()
    
    if st.button("🗂️ Archive Old Chats", use_container_width=True):
        # Archive chats older than 7 days
        cutoff_date = datetime.now() - datetime.timedelta(days=7)
        archived_count = 0
        
        sessions_to_remove = []
        for session_id, session_data in st.session_state.chat_sessions.items():
            if session_data["created_at"] < cutoff_date and session_id != st.session_state.current_session_id:
                sessions_to_remove.append(session_id)
                archived_count += 1
        
        for session_id in sessions_to_remove:
            del st.session_state.chat_sessions[session_id]
        
        if archived_count > 0:
            st.success(f"Archived {archived_count} old chats")
        else:
            st.info("No old chats to archive")
    
    # Chat History Section
    st.markdown('<div class="section-header">Chats</div>', unsafe_allow_html=True)
    
    # Sort sessions by creation time (newest first)
    sorted_sessions = sorted(
        st.session_state.chat_sessions.items(),
        key=lambda x: x[1]["created_at"],
        reverse=True
    )
    
    # Filter sessions based on search query
    if search_query:
        filtered_sessions = []
        for session_id, session_data in sorted_sessions:
            # Search in title and messages
            if search_query.lower() in session_data["title"].lower():
                filtered_sessions.append((session_id, session_data))
            else:
                # Search in message content
                for msg in session_data["messages"]:
                    if search_query.lower() in msg["content"].lower():
                        filtered_sessions.append((session_id, session_data))
                        break
        sorted_sessions = filtered_sessions
    
    # Display chat sessions
    for session_id, session_data in sorted_sessions:
        # Create a short title from first message or use default
        if session_data["messages"]:
            first_message = session_data["messages"][0]["content"]
            title = first_message[:35] + "..." if len(first_message) > 35 else first_message
        else:
            title = session_data["title"]
        
        # Highlight current session
        if session_id == st.session_state.current_session_id:
            st.markdown(f"**🔹 {title}**")
        else:
            if st.button(f"💭 {title}", key=f"session_{session_id}", use_container_width=True):
                st.session_state.current_session_id = session_id
                st.rerun()
        
        # Show message count and date
        msg_count = len(session_data["messages"])
        date_str = session_data["created_at"].strftime("%m/%d")
        st.caption(f"💬 {msg_count} messages • {date_str}")

# Get current session
current_session = st.session_state.chat_sessions[st.session_state.current_session_id]

# Main chat interface
st.title("💬 Smart Chat Assistant")

if api_error:
    st.error(f"🚫 **API Error:** {api_error}")
else:
    # Display chat messages from current session
    chat_container = st.container()
    with chat_container:
        for message in current_session["messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        if model is None:
            st.error("Failed to initialize AI model. Please check your API key configuration.")
        else:
            # Add user message to current session
            current_session["messages"].append({"role": "user", "content": prompt})
            
            # Update session title if it's the first message
            if len(current_session["messages"]) == 1:
                title = prompt[:35] + "..." if len(prompt) > 35 else prompt
                current_session["title"] = title
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate and display assistant response
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                
                try:
                    # Generate response from AI
                    with st.spinner("Thinking..."):
                        response = model.generate_content(prompt)
                        assistant_response = response.text
                    
                    # Display the response
                    message_placeholder.markdown(assistant_response)
                    
                    # Add assistant response to current session
                    current_session["messages"].append({
                        "role": "assistant", 
                        "content": assistant_response
                    })
                    
                except Exception as e:
                    error_message = f"Sorry, I encountered an error: {str(e)}"
                    message_placeholder.error(error_message)
                    
                    # Add error message to current session
                    current_session["messages"].append({
                        "role": "assistant", 
                        "content": error_message
                    })

# Footer
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: #666;'>
        <small>Smart Chat Assistant | Current: {current_session['title']}</small>
    </div>
    """, 
    unsafe_allow_html=True
)