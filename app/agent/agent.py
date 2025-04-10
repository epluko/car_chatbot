"""
utils/agent.py

Defines the agent graph.

functions:
- build_graph:  builds (compiles) the graph 
"""


from langgraph.graph import START, END, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.memory import MemorySaver

# from utils import ConversationState
# from utils import logger
from agent.utils import *




def build_graph() -> CompiledStateGraph:
    """Builds graph, compiles it and returns a ready to use agent graph object.
    The structure of the graph is HARDCODED in this function.
    """
    logger.debug("building graph ...")
    graph_memory = MemorySaver()
    graph_structure = StateGraph(ConversationState)
    # adding nodes
    graph_structure.add_node(WELCOME, welcome)
    graph_structure.add_node(HUMAN, human_feedback)
    graph_structure.add_node(AI, ai_response)
    graph_structure.add_node(CONCLUDE_PREF, conclude_car_preferences)
    graph_structure.add_node(SUMMARY, make_summary)
    graph_structure.add_node(Q_NEED_SUMMARY, q_need_summary)
    graph_structure.add_node(Q_WANT_FINISH, q_want_finish)
    # adding edges
    graph_structure.add_edge(START, WELCOME)
    graph_structure.add_edge(WELCOME, HUMAN)
    graph_structure.add_edge(HUMAN, Q_WANT_FINISH)
    graph_structure.add_conditional_edges(Q_WANT_FINISH, continue_chat)  # --> END | Q_NEED_SUMMARY
    graph_structure.add_conditional_edges(Q_NEED_SUMMARY, need_summary)  # -->  SUMMARY | CONCLUDE_PREF
    graph_structure.add_edge(CONCLUDE_PREF, AI)
    graph_structure.add_edge(SUMMARY, CONCLUDE_PREF)
    graph_structure.add_edge(AI, HUMAN)
    # building graph
    # for langgraph in memory checkpointer can't be used ... it's handled by the dev server
    # when working with demo app without postgres, checkpointer=graph_memory is required
    # graph = graph_structure.compile(interrupt_before=[HUMAN])
    graph = graph_structure.compile(interrupt_before=[HUMAN], checkpointer=graph_memory)
    
    # this works in Jupyter notebook - displays graph
    # display(Image(graph.get_graph(xray=1).draw_mermaid_png()))
    return graph


graph = build_graph()

graph_config = {"configurable": {"thread_id": "3"}}