

import streamlit as st
# st.session_state-> dictionary

# this we use it for invoking the chatbot (ie workflow.invoke )
from langgraph_backend import chatbot

from langchain_core.messages import HumanMessage

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

CONFIG = {'configurable': {'thread_id': 'thread_1'}}

# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

UserInput = st.chat_input('Type here')

if UserInput:
    # first add the message to st.session_state['message_history']
    st.session_state['message_history'].append(
        {'role': 'user', 'content': UserInput})
    with st.chat_message('user'):
        st.text(UserInput)

    with st.chat_message('AI'):
        ai_message = st.write_stream(
            messages_chuck.content for messages_chuck, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=UserInput)]},
                config=CONFIG,
                stream_mode='messages')
        )
    st.session_state['message_history'].append(
        {'role': 'user', 'content': ai_message})

# we are implementing this code inside chat_message('AI')
'''for messages_chuck, metadata in chatbot.stream(
    {'messages': [HumanMessage(content="what is the recepie of maggie")]},
    config={'configurable': {'thread_id': 'thread_1'}},
    stream_mode='messages'
):'''

# ************************************************************************************************************************************
# ROOT CODE
'''
stream= chatbot.stream(
    {'messages': [HumanMessage(content="what is the recepie of maggie")]},
    config={'configurable': {'thread_id': 'thread_1'}}
    stream_mode='messages'
)   # this object will give the message chuck and the metadata
'''

# Loop run the above code
# use the object and get the message_chunk and metadata output
'''
for messages_chuck, metadat in chatbot.stream(
    {'messages': [HumanMessage(content="what is the recepie of maggie")]},
    config={'configurable': {'thread_id': 'thread_1'}},
    stream_mode='messages'
):
    if messages_chuck.content:
        print(messages_chuck.content, end=' ', flush=True)

        '''
# implement this streaming in frontend part , but in streamlit we have to use 'st.write_stream'
