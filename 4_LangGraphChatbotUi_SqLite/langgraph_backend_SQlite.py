# implementation of memory for Chatbot in SQL database


from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, Literal
import operator
from typing import List, Annotated
# (BaseMessage will add the flexibility of using HM , SM, AI Message in ChatBot )
from langchain_core.messages import HumanMessage, BaseMessage
from dotenv import load_dotenv

# this is the major change we have to do ***************************************
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3


from langgraph.graph.message import add_messages
# add_messages is the built-in function to add messages to the state in langgraph which gives more flexibility for BaseMessage, instead of using operator.add


class ChatbotState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]


load_dotenv()
model = ChatOpenAI()


def chat_node(state: ChatbotState):
    # take user query from the state, send it to LLM , response store to state
    messages = state['messages']
    response = model.invoke(messages)
    # we have to pass the response as a list because in above messages is defined as List[BaseMessage]
    return {'messages': [response]}


# this is the major change we have to implement**************************
connection = sqlite3.connect(database='chatbot.db', check_same_thread=False)
# add Checkpointer
Checkpointer = SqliteSaver(conn=connection)


graph = StateGraph(ChatbotState)
# add nodes now
graph.add_node('chat_node', chat_node)
# Now add edges
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=Checkpointer)

# this is the changes which we need to extract all the threadid inside the list


def retrieve_all_threads():
    all_threads = set()
    for checkpoint in Checkpointer.list(None):
        # we have to get the unique thread_id
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)


'''
# test case after the sql server connection is done , This will automatically create a chatbot.db
CONFIG = {'configurable': {'thread_id': 'thread_id2'}}
response = chatbot.invoke(
    {'messages': [HumanMessage(content="what is my name")]},
    config=CONFIG
)

print(response)
'''
