"""
agent_app.py

Provides functions for the app to interact with the agent graph.

Functions:
- chat_welcome
- chat_iteration
"""


from langgraph.graph.state import CompiledStateGraph
from langgraph.pregel.io import AddableValuesDict
from langchain_core.messages import HumanMessage

from .utils import *



def chat_welcome(graph : CompiledStateGraph, graph_config : dict) -> str:
    """Initiates conversation with the agent.

    Args:
        graph: 
        graph_config:
            example: {"configurable": {"thread_id": str(st.session_state.id)}}

    Returns:
        str : welcome message from the agent.
    """
    response = graph.invoke({'messages': None,
                            'car_preference' : CarProperties(),
                            'test' : "initial",
                            'desc' : "..."
                            },
                            graph_config)
    return response["messages"][0].content


def chat_iteration(message_from_human : str, graph : CompiledStateGraph, graph_config : dict) -> AddableValuesDict:
    """Runs one graph interation (pushes graph forward from a breakpoint).
    
    Args:
        graph
        graph_config
            example: {"configurable": {"thread_id": str(st.session_state.id)}}
    Returns:
        dict : graph state
        Important:
            Not all keys from the graph state schema will be returned.
            Only values that were modified will be returned.
    """
    current_state = graph.get_state(graph_config)
    next_state = current_state.next

    logger.debug(f"Graph interrupted in the state of type {type(current_state)} with value:")
    logger.debug(current_state)
    logger.debug(f"next state: {next_state}")
    logger.info(f"user input: {message_from_human.strip()}")
    logger.debug(f"updating state with HUMAN message as node {HUMAN}")

    graph.update_state(graph_config,
                       {"messages" : [HumanMessage(content=message_from_human)]},
                       as_node=HUMAN)

    # pushing the graph forward
    # input=None is crutial ... if not the graph will start from the beginning
    logger.debug(f"pushing the graph forward ...")

    # invokes and returns a state
    return graph.invoke(None, graph_config)
