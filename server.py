import asyncio
from websockets.asyncio.server import serve

clientes_conectados = set()

async def echo(websocket):
    
    clientes_conectados.add(websocket)
    try:
        async for message in websocket:
            print(f"Mensaje recibido: {message}")
            try:
                with open("mensajes.txt", "a", encoding="utf-8") as f:
                    f.write(message + "\n")
            except Exception as e:
                print(f"Error al escribir en el archivo: {e}")
            
            
            for cliente in clientes_conectados:
                if cliente != websocket:  
                    await cliente.send(message)
    except Exception as e:
        print(f"Error con un cliente: {e}")
    finally:
        clientes_conectados.remove(websocket)  

async def main():
    async with serve(echo, "localhost", 8765):
        print("Servidor WebSocket escuchando en ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
