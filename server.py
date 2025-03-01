import asyncio
import websockets
import json

async def send_pose_data(websocket, path):
    while True:
        pose_data = {
            "shoulder": {"x": 0, "y": 1, "z": 0},
            "elbow": {"x": 0.5, "y": 0.5, "z": 0},
            "hand": {"x": 1, "y": 0, "z": 0}
        }
        await websocket.send(json.dumps(pose_data))
        await asyncio.sleep(0.1)

start_server = websockets.serve(send_pose_data, "0.0.0.0", 10000)  # Use port 10000

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()