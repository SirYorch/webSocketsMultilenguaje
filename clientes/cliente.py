import asyncio
from websockets.asyncio.client import connect

async def enviar(websocket):
    while True:
        try:
            mensaje = await asyncio.get_event_loop().run_in_executor(None, input, "Tú: ")
            await websocket.send(mensaje)
        except Exception as e:
            print(f"[ERROR al enviar] {e}")
            break

async def recibir(websocket):
    while True:
        try:
            mensaje = await websocket.recv()
            print(f"\nServidor: {mensaje}")
        except Exception as e:
            print(f"[ERROR al recibir] {e}")
            break

async def chat():
    try:
        async with connect("ws://localhost:8765") as websocket:
            print("Conectado al servidor.")
            await asyncio.gather(
                enviar(websocket),
                recibir(websocket)
            )
    except Exception as e:
        print(f"[ERROR de conexión] {e}")

if __name__ == "__main__":
    try:
        asyncio.run(chat())
    except KeyboardInterrupt:
        print("\nDesconectado por el usuario.")
