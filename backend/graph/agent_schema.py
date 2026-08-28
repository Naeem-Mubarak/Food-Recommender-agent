from typing import TypedDict,Optional,List,Literal,Annotated,Any
from pydantic import Field
import operator


# state the agent which will get updated throughout the flow 
class state_schema(TypedDict):

    text : str

    user_id : Optional[int]
    name : Optional[str]

    # evaluating the id and name 
    evaluator : Optional[Annotated[
        Literal['correct','in-correct'],
        Field(description='Evaluating the information given by customer correct or not')
        ]]  

    order : Optional[str]
    order_info : Optional[dict]

    # history can be a dict (if there is ) or can be list (if nothing is in history)
    history : Optional[dict[str , Any] | List[Any]]

    # either order_info is complete or not
    order_eval : Optional[Annotated[
        Literal['complete' , 'missing'],
        Field(description='Evaluate wether the order information is complete or not')
        ]]

    # Items suggested by agent
    recommendations : Annotated[
        Optional[List[dict]],
        Field(default=None)
    ]

    iteration : int

    recommendation_satisfaction : Optional[Annotated[
            Literal['yes','no'],
            Field(description='Is user satisfy with the recommendation')
        ]]

    rejected_recommendations : Annotated[
        Optional[List[dict]],
        operator.add
    ]

    selected_item : Optional[dict[Any,Any]]


    confirm_order : Optional[Annotated[
        Literal['confirm','not-confirm'],
        Field(description="Either order is confirm or not")
    ]]



