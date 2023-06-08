import asyncio
import websockets
import os
import subprocess
import json
import sys
import base64


async def run_script_reconocimiento(video):
    result = subprocess.run([sys.executable, 'C:/Users/eh180/OneDrive/Escritorio/python/facial-app/reconocimiento.py', video], capture_output=True, text=True)
    return result.stdout

async def run_script_entrenamiento():
    result = subprocess.run([sys.executable, 'C:/Users/eh180/OneDrive/Escritorio/python/facial-app/entrenamiento.py'], capture_output=True, text=True)
    return result.stdout

async def run_script_generar_imagenes(identificador, videopath):
    result = subprocess.run([sys.executable, 'C:/Users/eh180/OneDrive/Escritorio/python/facial-app/generar_imagenes.py', identificador, videopath], capture_output=True, text=True)
    return result.stdout

async def video(websocket, path):
    while True:
        try:
            with open('output.mp4', 'ab') as f:
            
                data = await websocket.recv()
                clave, video = json.loads(data)
                message = ""
                if clave == 'reconocimiento':
                    video_bytes =  bytes(video['data'])
                    f.write(video_bytes)
                    message = await run_script_reconocimiento('C:/Users/eh180/OneDrive/Escritorio/python/facial-app/output.mp4')
                    print(message)
                elif clave == 'generar':
                    nombre, videopath = video
                    message = await run_script_generar_imagenes(identificador=nombre, videopath=videopath)
                    await run_script_entrenamiento()

                await websocket.send(message)

        except websockets.exceptions.ConnectionClosedOK:
            print("El cliente ha cerrado la conexión.")
            try:
                await websocket.send("Se ha cerrado la conexión")  # Aquí es donde ocurre la excepción
            except websockets.exceptions.ConnectionClosedOK:
                print("La conexión ya está cerrada, no se puede enviar un mensaje.")
                break


start_server = websockets.serve(video, "localhost", 8765, max_size=100000000000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
