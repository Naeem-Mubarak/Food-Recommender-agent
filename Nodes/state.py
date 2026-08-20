from typing import TypedDict,Optional,List,Literal,Annotated,Any
from pydantic import Field


class state_schema(TypedDict):

    voice : str

    user_id : int
    name : str

    # evaluating the order info
    evaluator : Annotated[
        Literal['correct','in-correct'],
        Field(description='Evaluating the information given by customer either is correct or not')
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