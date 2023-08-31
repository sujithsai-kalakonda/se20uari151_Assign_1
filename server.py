import asyncio
import websockets

# Maintain a list of connected clients
connected_clients = set()

async def server(websocket, path):
    # Add the connected client to the set
    connected_clients.add(websocket)
    
    try:
        async for message in websocket:
            print(f"Received from client: {message}")
            
            # Broadcast the message to all connected clients
            for client in connected_clients:
                await client.send(f"Server received: {message}")
    except websockets.exceptions.ConnectionClosedError:
        pass
    finally:
        # Remove the client when they disconnect
        connected_clients.remove(websocket)

start_server = websockets.serve(server, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
