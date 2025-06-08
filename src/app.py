import streamlit as st
import ollama
import uuid
import json


DEFAULT_MODEL = "llama3.2:latest"
APP_TITLE = "LLM UI"
CHAT_SAVE_PATH = "saved-chats"
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

    return response["message"]["content"]

# TODO: Track full conversation history in the session state
# TODO: Make conversation history savable
# TODO: Make conversation history loadable from a file
# TODO: Restore session id on conversation load
# TODO: Log state and interactions to a file or database
# TODO: Handle reasoning model responses 

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

    # Chat area
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
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
                st.write(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
    # Run the app with: streamlit run src/app.py
    # Access the app at: http://localhost:8501
    # Stop the app with: Ctrl+C in the terminal
