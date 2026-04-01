import java.io.*;
import java.net.*;

public class ConnectionHandler implements Runnable {
    private final BCNode node;
    private final ServerSocket serverSocket;

    public ConnectionHandler(BCNode node, ServerSocket serverSocket) {
        this.node = node;
        this.serverSocket = serverSocket;
    }

    @Override
    public void run() {
        System.out.println("ConnectionHandler: waiting for incoming connections...");
        while (!serverSocket.isClosed()) {
            try {
                Socket s = serverSocket.accept();
                System.out.println("Accepted connection from " + s.getInetAddress().getHostAddress() + ":" + s.getPort());
                // On the server side, create ObjectInputStream BEFORE ObjectOutputStream
                ObjectInputStream ois = new ObjectInputStream(s.getInputStream());
                ObjectOutputStream oos = new ObjectOutputStream(s.getOutputStream());
                node.addPeerConnection(s, oos, ois);
            } catch (SocketException se) {
                // ServerSocket likely closed for shutdown
                System.out.println("ConnectionHandler shutting down.");
                break;
            } catch (IOException e) {
                System.err.println("Error in ConnectionHandler: " + e.getMessage());
            }
        }
    }
}
