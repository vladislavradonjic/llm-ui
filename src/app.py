import streamlit as st

DEFAULT_MODEL = "llama3.2:latest"
APP_TITLE = "LLM UI"


def get_model_response(chat_history):

    return "This is a test response."

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
