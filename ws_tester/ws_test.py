import asyncio
import websockets
import signal
import sys
import json

async def connect_to_websocket(url, open_data=None):
    async with websockets.connect(url) as websocket:
        try:
            if open_data:
                await websocket.send(json.dumps(open_data))
            
            while True:
                data = await websocket.recv()
                print(data)
        except websockets.ConnectionClosed:
            print("Connection closed.")

def signal_handler(sig, frame):
    print('Exiting...')
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    
    asyncio.get_event_loop().run_until_complete(
        connect_to_websocket(
            url="server_url",
            open_data={}
        )
    )