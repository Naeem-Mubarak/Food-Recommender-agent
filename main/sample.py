from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.types import Command
from config.system_info import DB_URL
from Graph.graph import graph
from models.English_translator import english_translator
from models.speech_to_text import voice_transcript_generator

with PostgresSaver.from_conn_string(DB_URL) as checkpointer:


    checkpointer.setup()

    agent = graph.compile(
        checkpointer=checkpointer
    )

    # Thread id
    config = {
        "configurable" : {
            "thread_id" : "123"
        }
    }


    path = r"/home/naeemmubarak/Desktop/Food Suggestion agent/test_output2.wav"

    initial_state = {
        'path' : path
    }

    result = agent.invoke(
        initial_state,
        config
    )

    while "__interrupt__" in result:

        interrupt_data = result["__interrupt__"][0].value

        print("\nBackend Message")
        print(interrupt_data)

        interrupt_type = interrupt_data["type"]

        if interrupt_type == 'New user':

            new_user_name = input("Enter your name: ")

            resume_value = {
                "name" : new_user_name
            }

        elif interrupt_type == 'order info collection':

            order_info = input("Enter what you want to eat and what is your budget:  ")

            resume_value = order_info

        elif interrupt_type == 'Select dish':

            dish_name = input("Select the dish you want to final: ")
            resume_value = dish_name

        elif interrupt_type == 'confirmation':

            confirmation = input("Do you want to confirm this order? (yes/no): ")
            resume_value = confirmation

        else:

            raise ValueError(f"Unknown interrupt type : {interrupt_type}")

        result = agent.invoke(
            Command(resume=resume_value),
            config
        )


print("Final result")

print(result)



