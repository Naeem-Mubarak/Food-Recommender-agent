from typing import TypedDict,Optional,List,Literal,Annotated,Any
from pydantic import Field
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


# state the agent which will get updated throughout the flow 
class state_schema(TypedDict):

    voice : str

    user_id : int | None = None
    name : str

    messages : Annotated[list[BaseMessage],add_messages]

    # evaluating the id and name 
    evaluator : Annotated[
        Literal['correct','in-correct'],
        Field(description='Evaluating the information given by customer correct or not')
        ]

    order : str
    order_info : Optional[dict]

    # history can be a dict (if there is ) or can be list (if nothing is in history)
    history : dict[str , Any] | List[Any]

    # either order_info is complete or not
    order_eval : Annotated[
        Literal['complete' , 'missing'],
        Field(description='Evaluate wether the order information is complete or not')
        ]

    recommendations : List[dict]

    selected_item : dict[Any,Any]

    confirm_order : Annotated[
        Literal['confirm','not-confirm'],
        Field(description="Either order is confirm or not")
    ]