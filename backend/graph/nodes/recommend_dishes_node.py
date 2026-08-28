from graph.agent_schema import state_schema
from database.menu_loader import menu_loader
from graph.schemas.recommend_dishes_schema import chain



def recommendation(state: state_schema):

    """Recommend 2 dishes on the basis of past data of the user (if exist) and current order requirements and then update the state for further processing"""

    # loading menu
    menu=menu_loader()

    recommendations=chain.invoke({
        'history':state['history'],
        'order':state['order'],
        'order_info' : state['order_info'],
        'rejected_dishes' : state['rejected_recommendations'],
        'menu': menu
    })

    dishes = recommendations.model_dump()

    # state updation
    state['recommendations'] = dishes['recommendations']
    state['iteration'] = state['iteration'] + 1

    # data user can see for each 
    select_data = ['restaurant_name','cuisine_type','dish_name','spice_level','dish_price','type_of_food','healthy_rating']

    filtered_dishes=[
    {k: item[k] for k in select_data if k in item}
    for item in dishes['recommendations']]

    print(filtered_dishes)


    return state