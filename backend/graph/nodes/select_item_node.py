from graph.agent_schema import state_schema
from langgraph.types import interrupt
from graph.schemas.select_item_schema import chain




def format_recommendations(dishes: list[dict]) -> str:
    """Turns the recommended dish list into a spoken instruction, so the
    user actually hears what their options are before being asked to pick."""
    lines = []
    for i, d in enumerate(dishes, start=1):
        lines.append(
            f"Option {i}: {d['dish_name']} from {d['restaurant_name']}, "
            f"spice level {d['spice_level']} out of five, "
            f"priced at {d['dish_price']} rupees."
        )
    return "Here are your options. " + " ".join(lines) + " Which one would you like?"




def select_item(state : state_schema):

    """
    accept user order if there is which is selected from the recommendations provided by the agent and then updates the state otherwise other nodes handle things in loop
    """

    instruction_text = format_recommendations(state['recommendations'])

    # interrputing flow to get the final order from the user
    item = interrupt({
        "type" : 'Select dish',
        "instruction" : instruction_text
    })

    state['text'] = item

    response = chain.invoke({
        'item' : state['text'],
        'menu' : state['recommendations']
    })

    # converting pydantic mode to dict so we can extract info easily
    user_response = response.model_dump()
    selected_dish = user_response['dish']

    # state updation
    state['selected_item'] = selected_dish
    state['recommendation_satisfaction'] = user_response['liked_recommendation']

    if selected_dish is not None:

        dish = user_response['data_of_dish']
        selected_dish_data = ['restaurant_name' , 'cuisine_type' , 'dish_name' , 'dish_price' , 'type_of_food']
        
        final_dish = [dish[dish_info] for dish_info in selected_dish_data]
        
        print(final_dish)


    return state



    







