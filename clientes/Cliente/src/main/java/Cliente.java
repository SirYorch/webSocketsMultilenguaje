import javax.websocket.*;
import java.net.URI;
import java.util.Scanner;

@ClientEndpoint
public class Cliente {

    private static Session session;

    public static void main(String[] args) {
        try {
            WebSocketContainer container = ContainerProvider.getWebSocketContainer();
            URI uri = new URI("ws://localhost:8765");
            container.connectToServer(Cliente.class, uri);
            System.out.println("✅ Conectado al servidor WebSocket.\n");

            // Hilo para leer desde consola y enviar
            Thread enviarThread = new Thread(() -> {
                Scanner scanner = new Scanner(System.in);
                while (true) {
                    System.out.print("Tú: ");
                    String mensaje = scanner.nextLine();
                    try {
                        session.getBasicRemote().sendText(mensaje);
                    } catch (Exception e) {
                        System.out.println("[❌ Error al enviar] " + e.getMessage());
                        break;
                    }
                }
            });
            enviarThread.start();

            // El hilo principal queda esperando en onMessage

        } catch (Exception e) {
            System.out.println("[❌ Error de conexión] " + e.getMessage());
        }
    }

    @OnOpen
    public void onOpen(Session session) {
        Cliente.session = session;
    }

    @OnMessage
    public void onMessage(String message) {
        System.out.println("\nServidor: " + message);
        System.out.print("Tú: "); // para que reaparezca después del mensaje del servidor
    }

    @OnClose
    public void onClose(Session session, CloseReason reason) {
        System.out.println("🔒 Conexión cerrada: " + reason);
    }

    @OnError
    public void onError(Session session, Throwable throwable) {
        System.out.println("[⚠️ Error]: " + throwable.getMessage());
    }
}
