# Code refactored from https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps

from openai import OpenAI
import streamlit as st

# Function to check if the API key is valid
def is_valid_api_key(api_key):
    # Add more specific validation logic if needed
    return len(api_key) == 64

# Sidebar title
with st.sidebar:
    st.title('rChatBot 👾')

    # Get the OpenAI API token from the user
    input_key = st.sidebar.text_input('Enter OpenAI API token:', type='password')

    # Check if the API key is provided and valid
    if input_key and is_valid_api_key(input_key):
        # Display a warning if the API key is too short
        st.warning('Invalid API key. Please enter a valid API key!', icon='👀')
    elif input_key:
        # Initialize the OpenAI client
        try:
            client = OpenAI(api_key=input_key)
            # Proceed to entering the prompt message
            st.success('API key is valid. Proceed to entering your prompt message!', icon='💁‍♂️')
        except Exception as e:
            # Display a warning if there's an issue during initialization
            st.warning(f'Error during OpenAI client initialization: {e}', icon='⚠️')
    else:
        # Display a message to enter the API key
        st.warning('Please enter your OpenAI API key!', icon='👀')

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
