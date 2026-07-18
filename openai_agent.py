from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from typing import Annotated

from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq

import os
from dotenv import load_dotenv

os.environ['GROQ_API_KEY']=os.getenv('GROQ_API_KEY')

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    
model=ChatGroq(model='llama-3.1-8b-instant', temperature=0)


def make_default_graph():
    graph_workflow=StateGraph(State)
    def call_model(state):
        return {'messages': [model.invoke(state['messages'])]}
    
    graph_workflow.add_node('agent', call_model)
    graph_workflow.add_edge('agent', END)
    graph_workflow.add_edge(START, 'agent')
    
    agent=graph_workflow.compile()
    
    return agent

agent=make_default_graph()