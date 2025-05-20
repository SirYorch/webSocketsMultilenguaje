import asyncio
from websockets.asyncio.server import serve

async def echo(websocket):
    async for message in websocket:
        print(f"Received message: {message}")
        
        # Guardar en archivo
        try:
            with open("mensajes.txt", "a", encoding="utf-8") as f:
                f.write(message + "\n")
        except Exception as e:
            print(f"Error al escribir en el archivo: {e}")

        await websocket.send(message)

async def main():
    async with serve(echo, "localhost", 8765) as server:
        print("Servidor WebSocket escuchando en ws://localhost:8765")
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
