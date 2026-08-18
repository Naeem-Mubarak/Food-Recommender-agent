from Nodes.state import state_schema

def check_completeness_node(state : state_schema):

    if state['order']=='None':

        print("interrupt and ask for order")

    elif state['order_info']['budget'] == 'None' or 0:

        print("Interrupt and ask the budget")

    elif state['order_info']['taste'] == 'None':

        print("Interrupt and ask for taste")

        
    



