import streamlit as st
import ollama
import uuid
import json
import re
from datetime import datetime


DEFAULT_MODEL = "llama3.2:latest"
APP_TITLE = "LLM UI"
CHAT_SAVE_PATH = "saved-chats"
LOGFILE_PATH = "logs/interaction_log.json"
SYSTEM_PROMPT = """
You are a helpful assistant that can answer questions and help with tasks.
When formulating your response you should use markdown formatting.
You should also consider the user's message history, provided below.
If you don't have enough information, just say "I don't know".
"""

def get_available_models() -> list[str]:
    """Fetch the list of available models from Ollama. 
    Returns:
        List of model names.
    """
    try:
        models = ollama.list()
        return [model["model"] for model in models["models"]]
    except Exception as e:
        st.error(f"Error fetching models: {e}")
        return []


def create_prompt(chat_history: list[dict]) -> list[dict]:
    """Create a prompt for the LLM based on the chat history.
    Args:
        chat_history: List of messages in the chat history.
    Returns:
        List of messages formatted for the LLM.
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for message in chat_history:
        messages.append({"role": message["role"], "content": message["content"]})

    return messages

  
def get_model_response(chat_history: list[dict]) -> str:
    """Get a response from the LLM based on the chat history.
    Args:
        chat_history: List of messages in the chat history.
    Returns:
        The response from the LLM.
    """
    messages = create_prompt(chat_history)
    response = ollama.chat(model=st.session_state.current_model, messages=messages)

    log_interaction(
        session_id=st.session_state.session_id,
        role=chat_history[-1]["role"] if chat_history else "user",
        query=chat_history[-1]["content"] if chat_history else "",
        prompt=json.dumps(messages, indent=2),
        response=response["message"]["content"]
    )

    return response["message"]["content"]

def log_interaction(session_id, role, query, prompt, response):
    """Log the interaction to a file or database.
    Args:
        session_id: Unique identifier for the session.
        role: Role of the user (e.g., "user", "assistant").
        query: User's query or message.
        prompt: Prompt sent to the model.
        response: Response from the model.
    """
    log_entry = {
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "role": role,
        "query": query,
        "prompt": prompt,
        "response": response
    }
    
    with open(LOGFILE_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")


def split_think_content(response: str):
    """
    Splits the response into 'thinking' (inside <think>...</think>) and 'message' (outside).
    Returns a tuple: (message, thinking)
    """
    think_pattern = re.compile(r"<think>(.*?)</think>", re.DOTALL | re.IGNORECASE)
    thinking = ""
    message = response
    match = think_pattern.search(response)
    if match:
        thinking = match.group(1).strip()
        # Remove the <think>...</think> part from the message
        message = think_pattern.sub("", response).strip()
    return message, thinking


def main():
    """Main function to run the Streamlit app."""
    # Configure the web app
    st.set_page_config(page_title=APP_TITLE, page_icon=":robot:")
    st.title(APP_TITLE)
    st.markdown(
        "This is a simple web app to interact with LLMs. "
        "You can select a model and start chatting."
    )

    # Initialize session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_model' not in st.session_state:
        st.session_state.current_model = DEFAULT_MODEL
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    # Sidebar
    with st.sidebar:
        st.markdown(f"**Session ID:** `{st.session_state.session_id}`")
        
        st.header("Options")

        models = get_available_models()
        st.session_state.current_model = st.selectbox(
            "Select Model",
            options=models,
            index=models.index(st.session_state.current_model) if st.session_state.current_model in models else 0,
            help="Choose the model you want to use for chatting."
        )

        if st.button("Reset Chat"):
            st.session_state.chat_history = []
            st.session_state.session_id = str(uuid.uuid4())
            st.toast("Chat history has been reset.")

        if st.button("Save Chat"):
            if len(st.session_state.chat_history) > 1:
                filename = f"{CHAT_SAVE_PATH}/chat_history_{st.session_state.session_id}.json"
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(st.session_state.chat_history, f, indent=4)
                st.toast(f"Chat history saved to `{filename}`.")
            else:
                st.toast("No chat history to save.")

        uploaded_history = st.file_uploader("Load Chat", type=["json"], label_visibility="collapsed")
        if uploaded_history is not None:
            try:
                chat_history = json.load(uploaded_history)
                # validate chat history format
                if isinstance(chat_history, list) and all(
                    isinstance(msg, dict) and "role" in msg and "content" in msg for msg in chat_history
                ):
                    st.session_state.chat_history = chat_history
                    st.session_state.session_id = str(uuid.uuid4())
                    st.toast("Chat history loaded successfully.")
                else:
                    st.toast("Invalid chat history format.")
            except Exception as e:
                st.toast(f"Error loading chat history: {e}")

    # Chat area
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            # Only process <think> tags for assistant messages
            if message["role"] == "assistant":
                msg, thinking = split_think_content(message["content"])
                if thinking:
                    # Use Streamlit's expander for optional thinking display
                    st.write(msg)
                    with st.expander("Show model reasoning"):
                        st.markdown(thinking)
                else:
                    st.write(message["content"])
            else:
                st.write(message["content"])

    # Input area
    user_input = st.chat_input("Enter your message here...")

    if user_input:
        # Append user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.write(user_input)

        # Get show response
        with st.spinner("Generating response..."):
            # Simulate a response from the model
            response = get_model_response(st.session_state.chat_history)
            with st.chat_message("assistant"):
                msg, thinking = split_think_content(response)
                if thinking:
                    st.write(msg)
                    with st.expander("Show model reasoning"):
                        st.markdown(thinking)
                else:
                    st.write(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
    # Run the app with: streamlit run src/app.py
    # Access the app at: http://localhost:8501
    # Stop the app with: Ctrl+C in the terminal
