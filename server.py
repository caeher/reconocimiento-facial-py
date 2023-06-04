import asyncio
import websockets
import os

async def video(websocket, path):
    while True:
        try:
            with open('output.webm', 'ab') as f:
            
                data = await websocket.recv()
                f.write(data)
                print(f"Recibido y escrito {len(data)} bytes")
                greeting = f"Hello!"
                await websocket.send(greeting)
        except websockets.exceptions.ConnectionClosedOK:
            print("El cliente ha cerrado la conexión.")
            try:
                await websocket.send("Se ha cerrado la conexión")  # Aquí es donde ocurre la excepción
            except websockets.exceptions.ConnectionClosedOK:
                print("La conexión ya está cerrada, no se puede enviar un mensaje.")
                break


start_server = websockets.serve(video, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
