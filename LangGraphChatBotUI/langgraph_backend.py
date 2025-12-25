# Here we are using the same Skeleton of chatbot and improving it by adding loops and conditions to store the chat history.
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, Literal
import operator
from typing import List, Annotated
# (BaseMessage will add the flexibility of using HM , SM, AI Message in ChatBot )
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver

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


# add Checkpointer
Checkpointer = MemorySaver()

graph = StateGraph(ChatbotState)

# add nodes now
graph.add_node('chat_node', chat_node)
# Now add edges
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=Checkpointer)
