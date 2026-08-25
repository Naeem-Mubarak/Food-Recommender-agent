import uuid
from fastapi import FastAPI,WebSocket
from contextlib import asynccontextmanager
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.types import Command
from config.system_info import DB_URL
from graph.graph import graph
from graph.initial_state import initial_state

from models.text_to_speech import text_to_speech
from models.speech_to_text import voice_transcript_generator



agent = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global agent
    # enter the context manager manually and keep it open
    with PostgresSaver.from_conn_string(DB_URL) as checkpointer:
        checkpointer.setup()
        agent = graph.compile(checkpointer=checkpointer)
        yield   # server runs here, connection stays open the whole time
    # code after yield runs on shutdown - connection closes cleanly



app = FastAPI(lifespan=lifespan)




@app.websocket("/agent")
async def food_recommendation_agent(websocket : WebSocket):

    await websocket.accept()


    # new thread at every run
    config = {
        "configurable" : {
            "thread_id" : str(uuid.uuid4())
        }
    }

    # invoking agent with empty state
    result = await agent.ainvoke(
        initial_state(),
        config
    )

    # handling interrupts
    while "__interrupt__" in result:

        interrupt_data = result["__interrupt__"][0].value


        # agent reply
        agent_response = await text_to_speech(interrupt_data['instruction'])

        # sending agent's reply to the user
        await websocket.send_bytes(agent_response)

        # receiving user's response
        voice = await websocket.receive_bytes()
        # converting user's voice to text
        text = await voice_transcript_generator(voice)

        # resuming workflow after getting user response
        result = await agent.ainvoke(
            Command(resume=text),
            config
        )



