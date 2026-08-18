from typing import TypedDict,Optional,List,Literal,Annotated
from pydantic import Field


class state_schema(TypedDict):

    voice : str
    user_id : int
    name : str
    evaluator : Annotated[Literal['correct','in-correct'],Field(description='Evaluating the information given by customer either is correct or not')]
    order : str
    order_info : Optional[dict]
    history : Optional[dict]

    recommendations : List[dict]










# graph=StateGraph(state_schema)
# graph.add_node('cust_order',voice_receiver)
# graph.add_node('history',history)
# graph.add_node('recommend',select_item)

# graph.add_edge(START,'cust_order')
# graph.add_edge('cust_order','history')
# graph.add_edge('history','recommend')
# graph.add_edge('recommend',END)

# workflow=graph.compile()

# path=r"/home/naeemmubarak/Desktop/Food Suggestion agent/sample.ogg"

# output=workflow.invoke({
#     'path':path
# })


# print(output)

