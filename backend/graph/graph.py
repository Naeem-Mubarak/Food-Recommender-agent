from langgraph.graph import START,END,StateGraph
from graph.agent_schema import state_schema
from graph.nodes.voice_receiver_node import reciever_node
from graph.nodes.Check_user_node import check_user
from graph.nodes.history_loader_node import history_loader
from graph.nodes.Check_completeness_node import check_completeness_node
from graph.nodes.recommend_dishes_node import recommendation
from graph.nodes.select_item_node import select_item
from graph.nodes.conditional_node import conditional_node
from graph.nodes.new_user_node import new_user
from graph.nodes.order_info_completion_node import order_info_completion
from graph.nodes.complete_info_node import complete_info
from graph.nodes.order_confirmation import confirmation_node
from graph.nodes.update_db_node import update_db
from graph.nodes.router import router
from graph.nodes.confirm_order import order_confirmation
from graph.nodes.order_collection_node import order_collection

graph=StateGraph(state_schema)


# Nodes of the Graph
graph.add_node('data_receiver',reciever_node)
graph.add_node('check_user',check_user)
graph.add_node('history_loader',history_loader)
graph.add_node('check_order_completness',check_completeness_node)
graph.add_node('recommendations',recommendation)
graph.add_node('select_item',select_item)
graph.add_node('new_user',new_user)
graph.add_node('complete_info',complete_info)
graph.add_node('update_db',update_db)
graph.add_node('order_confirmation',order_confirmation)
graph.add_node('order_collection',order_collection)


# Edges of the graph
graph.add_edge(START,'data_receiver')
graph.add_conditional_edges('data_receiver',router)
graph.add_conditional_edges('check_user',conditional_node)
graph.add_edge('new_user','check_user')
graph.add_edge('history_loader','order_collection')
graph.add_edge('order_collection','check_order_completness')
graph.add_conditional_edges('check_order_completness',order_info_completion)
graph.add_edge('complete_info','check_order_completness')
graph.add_edge('recommendations','select_item')
graph.add_edge('select_item', 'order_confirmation')
graph.add_conditional_edges('order_confirmation',confirmation_node)
graph.add_edge('update_db',END)


