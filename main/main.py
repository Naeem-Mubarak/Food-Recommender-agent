from langgraph.graph import START,END,StateGraph
from Nodes.state import state_schema
from Nodes.voice_receiver_node import voice_receiver
from Nodes.Check_user_node import check_user
from Nodes.history_loader_node import history_loader
from Nodes.Check_completeness_node import check_completeness_node
from Nodes.recommend_dishes_node import recommendation
from Nodes.select_item_node import select_dish
from Nodes.conditional_node import conditional_node
from Nodes.new_user_node import new_user
from Nodes.order_info_completion_node import order_info_completion
from Nodes.complete_info_node import complete_info
from Nodes.order_confirmation import confirmation_node
from Nodes.update_db_node import update_db

graph=StateGraph(state_schema)

graph.add_node('data_receiver',voice_receiver)
graph.add_node('check_user',check_user)
graph.add_node('history_loader',history_loader)
graph.add_node('check_order_completness',check_completeness_node)
graph.add_node('recommendations',recommendation)
graph.add_node('select_item',select_dish)
graph.add_node('new_user',new_user)
graph.add_node('complete_info',complete_info)
graph.add_node('update_db',update_db)


graph.add_edge(START,'data_receiver')
graph.add_edge('data_receiver','check_user')
graph.add_conditional_edges('check_user',conditional_node)
graph.add_edge('new_user','check_user')
graph.add_edge('check_user','history_loader')
graph.add_edge('history_loader','check_order_completness')
graph.add_conditional_edges('check_order_completness',order_info_completion)
graph.add_edge('complete_info','check_order_completness')
graph.add_edge('check_order_completness','recommendations')
graph.add_edge('recommendations','select_item')
graph.add_conditional_edges('select_item',confirmation_node)
graph.add_edge('update_db',END)



agent=graph.compile()