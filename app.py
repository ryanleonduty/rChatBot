# Code refactored from https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps

from openai import OpenAI
import streamlit as st

with st.sidebar:
    st.title('rChatBot 👾')
# Get the OpenAI API token from the user
    input_key = st.sidebar.text_input('Enter OpenAI API token:', type='password')
    if input_key:
    # Check if the API key is provided
        st.success('API key already provided!', icon='👍')
    # Initialize the OpenAI client
        client = OpenAI(api_key=input_key)
    # Proceed to entering the prompt message
        st.success('Proceed to entering your prompt message!', icon='💁‍♂️')
    else:
    # Display a warning if the API key is not provided
        st.warning('Please enter your key!', icon='👀')


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
