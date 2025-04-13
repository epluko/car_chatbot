"""
utils/nodes.py

Provides nodes and edges functions for the agent graph.
"""


from langgraph.graph import START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, AnyMessage, RemoveMessage
# from IPython.display import Image, display
from typing import Annotated, Literal
from .state import ConversationState, WantToContinue
from .data_schemas import CarProperties
from .logger import logger
from .llm import LLM



# Helper functions

def logger_debug_basic(state : ConversationState,
                       name : str,
                       obj_type : Literal['node', 'edge'] = 'node') -> None:
    """Creates basic logging record for langgraph nodes and edges
    """
    logger.debug(f"-->[{obj_type}] : {name}")
    logger.debug(f"state id is {id(state)}")
    logger.debug(f"state.car_preference id is {id(state.car_preference)}")
    logger.debug(f"state.car_preferences: {state.car_preference}")


GENERAL_SYSTEM_PROMPT = """
You are helpful assistant for a car retailing company in Europe. Your name is Stefan.
Your role is to chat with a customer and collect information about customer's car preference.
"""


def general_system_message_with_summary(state : ConversationState) -> list[SystemMessage]:
    """Creates and returns a list system messages consists of the general system prompt and a summary.
    """
    system_messages = [state.general_system_message]
    if state.summary:
        system_messages.append(state.summary)
        system_messages.append(SystemMessage(content="Use summary of earlier conversation."))
    return system_messages



# Nodes names as constants
# defined for better code readibility
WELCOME = "Welcome"
HUMAN = "Human"
AI = "AI_response"
CONCLUDE_PREF = "Conclude_car_preferences"
Q_WANT_FINISH = "Q-want_finish"
NEED_SUMMARY = "Need_summary"
Q_NEED_SUMMARY = "Q-need_summary"
SUMMARY = "Make_summary"
CONTINUE_CHAT = "Continue_chat"


WELCOME
def welcome(state: ConversationState):
    welcome_task_prompt = """
New customer has just entered the chat room.
Welcome the customer with short message.
Introduce yourself.
Encourage to the discussion about cars.
""".strip()
    logger_debug_basic(state, WELCOME, "node")
    general_system_message = SystemMessage(content=GENERAL_SYSTEM_PROMPT)
    system_message = SystemMessage(content=welcome_task_prompt)
    ai_message = LLM.invoke([general_system_message, system_message])
    return {'messages' : [ai_message], "general_system_message" : general_system_message}


HUMAN
def human_feedback(state: ConversationState):
    logger_debug_basic(state, HUMAN, "node")
    pass


AI
def ai_response(state: ConversationState):
    logger_debug_basic(state, AI, "node")
    system_messages = general_system_message_with_summary(state)
    system_messages.append(SystemMessage(
        content="""
            Respond to the customer in a way that is succinct, precise, professional, and polite.
            If the customer’s message is off-topic or irrelevant,
                acknowledge it courteously and guide the conversation back to the main topic.
            Keep your response under 100 words.
            """
        ))
    ai_message = LLM.invoke(system_messages + state.messages)
    return {'messages' : ai_message}  # I can return ai_message without a list dues to reducer modification


CONCLUDE_PREF
def conclude_car_preferences(state: ConversationState):
    logger_debug_basic(state, CONCLUDE_PREF, "node")
    llm_structured = LLM.with_structured_output(CarProperties)
    system_messages = general_system_message_with_summary(state)
    system_messages.append(SystemMessage(content="CAR PREFERENCE CONCLUDED EARLIER: " + state.car_preference.model_dump_json()))
    system_messages.append(
        SystemMessage(content="""
            Instrunction:
            1. Analyze latest communication with customer and summary of earlier communication if provided.
            2. Update customer's car preferences only if it clearly comes from the communication and summary.
            3. If you can't conclude particular information directly from the communication, try to conclude it from other concluded parameters e.g. type of car body can be derived from car model.
            4. Update customers preferences only if you are sure. Do not hallucinate.
            5. Do not update customers preference if you have more then one concluded options to choose.
        """)
    )
    logger.debug("messages to be passed to llm to conclude car preference:")
    for m in system_messages + state.messages:
        logger.debug(f"{m}")
    result = llm_structured.invoke(system_messages + state.messages)
    logger.debug(f"concluded car_preference:")
    logger.debug(f"car_pref values: {result}")
    logger.debug(f"car_pref type: {type(result)}")
    logger.debug(f"car_pref id: {id(result)}")
    # >>>>>> test
    # this line below will not modify graph state ... we need to return test - result???
    # state.test = "modified"
    return {"car_preference" : result, "test" : "modified"}


CONTINUE_CHAT
NUM_OF_MESSAGES_TO_EVALUATE = 3
def continue_chat(state: ConversationState) -> Literal[Q_NEED_SUMMARY, END]:
    logger_debug_basic(state, CONTINUE_CHAT, "edge")
    system_messages = [state.general_system_message]
    system_messages.append(
        SystemMessage(content="""
            Evaluate if customer wants to continue chat.
            Conclude False i.e. customer does not want to continue only if he expressed his will to finish.
        """.strip()))
    llm_structured = LLM.with_structured_output(WantToContinue)
    messages = state.messages[-3:] if len(state.messages) > NUM_OF_MESSAGES_TO_EVALUATE else state.messages
    result = llm_structured.invoke(system_messages + messages)
    if result.want_to_continue:
        logger.debug(f"go to: {CONCLUDE_PREF}")
        return Q_NEED_SUMMARY
    else:
        logger.debug(f"go to: {END}")
        return END


NUM_OF_MESSAGES_TO_SUMMARY = 4
NUM_OF_MESSAGES_TO_INITIATE_SUMMARY = 6
def need_summary(state : ConversationState) -> Literal[CONCLUDE_PREF, SUMMARY]:
    logger_debug_basic(state, NEED_SUMMARY, "edge")
    num_of_messages = len(state.messages)
    logger.debug(f"number of messages in the history: {num_of_messages}")
    if num_of_messages >= NUM_OF_MESSAGES_TO_INITIATE_SUMMARY:
        logger.debug(f"need to trim message memory -> going to summary")
        return SUMMARY
    return CONCLUDE_PREF


SUMMARY
def make_summary(state : ConversationState):
    logger_debug_basic(state, SUMMARY, "node")
    messages = general_system_message_with_summary(state)
    messages.extend(state.messages[:NUM_OF_MESSAGES_TO_SUMMARY])
    messages.append(SystemMessage(content = "Create summary of all human and AI messages. Be succinct. Return only summary."))
    ai_message = LLM.invoke(messages)
    new_summary = SystemMessage(content="SUMMARY OF EARLIER COMMUNICATION WITH CUSTOMER: " + ai_message.content)
    logger.debug(f"current summary: {state.summary}")
    logger.debug(f"new summary to be returned: {new_summary}")
    delete_messages = [RemoveMessage(m.id) for m in state.messages[:NUM_OF_MESSAGES_TO_SUMMARY]]
    logger.debug(f"delete messages: {[m.id for m in delete_messages]}")
    return {"summary" : new_summary, "messages" : delete_messages}


Q_NEED_SUMMARY
def q_need_summary(state : ConversationState):
    """Dummy node, helps to connect two conditional edges.
    It is presented as a decision point on the graph.
    """
    pass


Q_WANT_FINISH
def q_want_finish(state : ConversationState):
    """Dummy node, helps to better present conditional edge.
    It is presented as a decision point on the graph.
    """
    pass