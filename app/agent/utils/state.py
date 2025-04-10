"""
utils/state.py

Provides data schemas used as state schemas in the langgraph graph.

The schemas are based on Pydantic model.

Defined states (data schemas):
- ConversationState: main state
- WantToContinue: a simple state used to navigate the graph

"""


from langchain_core.messages import AnyMessage, SystemMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel
from typing import Annotated
from .data_schemas import CarProperties
from .logger import logger




# Reducers

def add_messages_with_None(left: list[AnyMessage] | None, right: list[AnyMessage] | AnyMessage | None) -> list[AnyMessage]:
    """Combines two lists of messages handling cases with None.

    Returns:
        list: A new list containing all elements from both input lists.
               If an input is None, it's treated as an empty list.
    """
    logger.debug(f"reducer:add_messages_with_None")
    left = left if left else []
    right = right if right else []
    right = right if type(right) is list else [right]
    return add_messages(left,right)

def set_car_preference(left: CarProperties | None, right: CarProperties) -> CarProperties:
    """Assigns values from one CarPreferences object to another one handling None.
    """
    logger.debug(f"reducer:set_car_preference")
    logger.debug(f"reducer:left: [{left}] with id {id(left)}")
    logger.debug(f"reducer:right orig: [{right}] with id {id(right)}")
    right = right if right else CarProperties()
    logger.debug(f"reducer:right: [{right}] with id {id(right)}")
    to_be_returned = right.model_copy()
    logger.debug(f"reducer:return: [{to_be_returned}] with id {id(to_be_returned)}")
    return to_be_returned


# Graph data schemas

class ConversationState(BaseModel):
    """Main state for the agent graph.
    """
    general_system_message : SystemMessage | None = None
    messages : Annotated[list[AnyMessage], add_messages_with_None] = []
    summary : SystemMessage | None = None
    car_preference : Annotated[CarProperties, set_car_preference]= CarProperties()
    test : str | None = None
    desc : str | None = None


class WantToContinue(BaseModel):
    """Simple state that helps to navigate hte graph.
    """
    want_to_continue : bool