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

    # here in the below source code of chatbot of 9A
    # we are using chatbot.invoke instead of workflow.invoke , so pass the messages inside the chatbot
    response = chatbot.invoke(
        {'messages': [HumanMessage(content=UserInput)]}, config=CONFIG)

    ai_message = response['messages'][-1].content

    # first add the message to st.session_state['message_history']
    st.session_state['message_history'].append(
        {'role': 'AI', 'content': ai_message})
    with st.chat_message('AI'):
        st.text(ai_message)


# this is the chatbot invoke code which we are going to use in above code
'''thread_id='1'
while True:
    user_message=input("TypeHere: ")
    print("User:",user_message)
    if user_message.lower() in ['exit','quit','bye']:
        print("Chatbot: Goodbye!")
        break
    config={'configurable':{'thread_id':thread_id}}
    response=workflow.invoke({'messages':[HumanMessage(content=user_message)]},config=config)
    print("AI:",response['messages'][-1].content)
'''


# This doesn't have streaming so we are implementing the streaming in 2_LangGraphChatbot_with_Streaming
