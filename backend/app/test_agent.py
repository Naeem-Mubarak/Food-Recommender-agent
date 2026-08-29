import asyncio
import websockets


async def test_agent():

    uri = "ws://127.0.0.1:8000/agent"

    i=0

    async with websockets.connect(uri) as websocket:

        while True:

            response = await websocket.recv()

            if isinstance(response, bytes):

                print("Received voice response")

                i+=1

                filename = f"agent_response_{i}.mp3"
                with open(filename, "wb") as f:
                    f.write(response)

                print("Saved: agent_response.mp3")

                message = input("You: ")

                await websocket.send(message)

            else:

                print("Agent JSON:", response)


asyncio.run(test_agent())