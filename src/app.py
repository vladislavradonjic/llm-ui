import streamlit as st
import ollama

DEFAULT_MODEL = "llama3.2:latest"
APP_TITLE = "LLM UI"
SYSTEM_PROMPT = """
You are a helpful assistant that can answer questions and help with tasks.
When formulating your response you should use markdown formatting.
You should also consider the user's message history, provided below.
If you don't have enough information, just say "I don't know".
"""

def get_model_response(chat_history):
    
    # Prepare the prompt
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for message in chat_history:
        messages.append({"role": message["role"], "content": message["content"]})

    response = ollama.chat(model=DEFAULT_MODEL, messages=messages)
    return response["message"]["content"]

def main():

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

    # Sidebar
    with st.sidebar:
        st.header("Options")

        if st.button("Reset Chat"):
            st.session_state.chat_history = []
            st.info("Chat history has been reset.")

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
