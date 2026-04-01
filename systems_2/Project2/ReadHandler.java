import java.io.*;

public class ReadHandler implements Runnable {
    private final BCNode node;
    private final BCNode.PeerConnection peer; // access to streams

    public ReadHandler(BCNode node, BCNode.PeerConnection peer) {
        this.node = node;
        this.peer = peer;
    }

    @Override
    public void run() {
        System.out.println("ReadHandler started for peer " + peer.id);
        try {
            while (true) {
                Object obj;
                try {
                    obj = peer.ois.readObject();
                } catch (EOFException eof) {
                    System.out.println("Peer " + peer.id + " closed connection.");
                    node.removePeer(peer.id);
                    break;
                }
                if (obj == null) continue;
                node.handleIncoming(obj, peer);
            }
        } catch (IOException | ClassNotFoundException e) {
            System.out.println("Connection to peer " + peer.id + " lost: " + e.getMessage());
            node.removePeer(peer.id);
        }
    }
}
