# implementation of resume chat with the specific threads in Chatbot

import streamlit as st
# st.session_state-> dictionary

# this we use it for invoking the chatbot (ie workflow.invoke )
from langgraph_backend import chatbot

from langchain_core.messages import HumanMessage

import uuid

# *******************************************Utility function********************************************


def generate_threadid():  # this will generate the random thread_id
    thread_id = uuid.uuid4()
    return thread_id

# when we click on the NewChat it has to do the below functionalities
# *generate a new thread_id
# *save it in session
# *reset message history


def reset_chat():
    thread_id = generate_threadid()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])  # B
    st.session_state['message_history'] = []


# this function will add the threadid to the 'chat_threads' in st.session
def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)


# this function will load all the convesation associated with the threadId
def load_conversation(thread_id):
    return chatbot.get_state(config={'configurable': {'thread_id': thread_id}}).values['messages']


# ************************************************session setup********************************************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_threadid  # add it to the session

if 'chat_threads' not in st.session_state:  # initializing the chat_thread in st.session_state
    st.session_state['chat_threads'] = []

add_thread(st.session_state['thread_id'])  # A

CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

# ***********************************************SidebarUI*****************************************************
# add a sidebar with title + A Start Chat Button + A title named 'My Conversations'
st.sidebar.title("LangGraph Chatbot")

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversation')

# to display all the thread id in side bar , use for loop
for thread_id in st.session_state['chat_threads'][::-1]:  # C
    if st.sidebar.button(str(thread_id)):    # D convertin it to button
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        # here the problem is the messages is different format not the role and content so use for loop for messages and assign the role and display
        temp_message = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
            temp_message.append({'role': role, 'content': msg.content})

        # assigning the new format to the original message_history
        st.session_state['message_history'] = temp_message


# ****************************************************Main UI**************************************************
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


'''
add a sidebar with title + A Start Chat Button + A title named 'My Conversations'
generate dynamic thread Id and add it to the session   ---------------------------> for this use library uuid
Display the thread id in sidebar 

*************************************************************************

On Click of new chat open a new chat window
    *generate a new thread_id
    *save it in session
    *reset message history

*****************************************************************************
create a list to store all thread_ids ( we have to generate the threadid in 2 cases, 1: when page refresh, 2:when we click on New Chat , in code refer A and B for this)
Load all the thread ids in the sidebar  ( in code its  refer as C)
convert the side bar text to clickable buttons  ( in code its  refer as D)

*********************************************************************************

on click of a particular thread id load that particular conversation

'''
