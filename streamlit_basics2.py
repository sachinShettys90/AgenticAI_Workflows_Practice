# Part 1 : building a copycat chatbot
import streamlit as st
''' 


with st.chat_message('User'):
    st.text('Hi')

with st.chat_message('assistant'):
    st.text('How can i help you?')

user_input = st.chat_input('Type_here')

if user_input:
    with st.chat_message('user'):
        st.text(user_input)
if user_input:
    with st.chat_message('assistant'):
        st.text(user_input)    '''

# here the problem is it will not store any of the chat ,when we enter it will automatically rerun the entire script
# so for that store the data inside the dictionary


# *****************************************************************************************************************************************


# Part2: the above same copycat bot with message history and display the message_history
'''
import streamlit as st

message_history = []  # creating the new empty list

# loading the conversation history
for messages in message_history:     # to display all the message history list
    with st.chat_message(messages['role']):
        st.text(messages['content'])

user_input = st.chat_input('Type_here')

if user_input:
    # adding the message of the user with role inside the message_history
    message_history.append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)
if user_input:
    # adding the message of the assistant with role inside the message_history
    message_history.append({'role': 'assistant', 'content': user_input})
    with st.chat_message('assistant'):
        st.text(user_input)

'''
# by using the above code the message history is getting deleted every time so we have to use the session state in the streamlit so that it will retain until we refresh the page


# part3
# so instead of message_history list use the session_state list with the key 'message_history' and pass the values

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []  # creating the empty list

# loading the conversation history
# to display all the message history list
for messages in st.session_state['message_history']:
    with st.chat_message(messages['role']):
        st.text(messages['content'])

user_input = st.chat_input('Type_here')

if user_input:
    # adding the message of the user with role inside the message_history
    st.session_state['message_history'].append(
        {'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)
if user_input:
    # adding the message of the assistant with role inside the message_history
    st.session_state['message_history'].append(
        {'role': 'assistant', 'content': user_input})
    with st.chat_message('assistant'):
        st.text(user_input)
