import java.io.*;
import java.net.*;
import java.util.*;
import java.util.concurrent.*;

public class BCNode {
    private final List<Block> chain = new ArrayList<>();
    // Map of peer address (host:port) to PeerConnection
    private final Map<String, PeerConnection> peers = new ConcurrentHashMap<>();
    private final int mineDifficulty; // number of leading zeros
    private final int myPort;
    private ServerSocket serverSocket;
    private volatile boolean running = true;

    // Simple holder for streams and socket
    static class PeerConnection {
        Socket socket;
        ObjectOutputStream oos;
        ObjectInputStream ois;
        String id; // host:port
        PeerConnection(Socket s, ObjectOutputStream oos, ObjectInputStream ois, String id) {
            this.socket = s; this.oos = oos; this.ois = ois; this.id = id;
        }
    }

    public BCNode(int myPort, List<Integer> remotePorts, int mineDifficulty) throws IOException {
        this.myPort = myPort;
        this.mineDifficulty = mineDifficulty;
        // create genesis block
        chain.add(new Block()); // genesis with default data
        // start server to accept incoming connections
        startServer();
        // connect to remote peers (clients)
        connectToRemotes(remotePorts);
        // obtain chain from peers (if any)
        if (!peers.isEmpty()) {
            // pick first peer and ask for chain by reading/writing - we will send/receive chain in constructor of peer read handler
            requestChainsFromPeers();
        }
    }

    private void startServer() throws IOException {
        serverSocket = new ServerSocket(myPort);
        Thread acceptThread = new Thread(new ConnectionHandler(this, serverSocket));
        acceptThread.setDaemon(true);
        acceptThread.start();
    }

    private void connectToRemotes(List<Integer> remotePorts) {
        for (Integer p : remotePorts) {
            if (p == myPort) continue;
            try {
                Socket s = new Socket("127.0.0.1", p);
                // Important: create ObjectOutputStream BEFORE ObjectInputStream on client side
                ObjectOutputStream oos = new ObjectOutputStream(s.getOutputStream());
                ObjectInputStream ois = new ObjectInputStream(s.getInputStream());
                String id = s.getInetAddress().getHostAddress() + ":" + p;
                PeerConnection pc = new PeerConnection(s, oos, ois, id);
                peers.put(id, pc);
                // spawn read handler thread
                Thread rh = new Thread(new ReadHandler(this, pc));
                rh.setDaemon(true);
                rh.start();
                System.out.println("Connected to remote node: " + id);
                // Immediately send our chain to the new peer so they can adopt/compare
                synchronized (pc.oos) {
                    pc.oos.writeObject(new ArrayList<>(chain));
                    pc.oos.reset();
                }
            } catch (IOException e) {
                System.err.println("Could not connect to remote port " + p + " : " + e.getMessage());
            }
        }
    }

    private void requestChainsFromPeers() {
        // We'll ask each peer for its chain by relying on the ReadHandler to send us a chain when connected.
        // If peers don't proactively send chain, an incoming chain will arrive later.
    }

    // Add block: chain previous hash, mine, validate, add, and broadcast
    public void addBlock(Block b) {
        synchronized (chain) {
            // set previous hash from last block
            String lastHash = chain.get(chain.size() - 1).getHash();
            b.setPreviousHash(lastHash);
            // recompute hash after setting previous hash
            b.setHash(b.calculateBlockHash());
            // mine
            mineBlock(b, mineDifficulty);
            // validate block against chain and add
            if (validateBlock(b, chain)) {
                chain.add(b);
                System.out.println("Block mined and added to local chain:");
                System.out.println(b);
                broadcastObject(b);
            } else {
                System.out.println("Mined block failed validation and was not added.");
            }
        }
    }

    private void mineBlock(Block b, int difficulty) {
        String prefixZeros = new String(new char[difficulty]).replace('\0', '0');
        System.out.println("Mining block... difficulty=" + difficulty + " (looking for prefix " + prefixZeros + ")");
        while (true) {
            String hash = b.calculateBlockHash();
            if (hash.startsWith(prefixZeros)) {
                b.setHash(hash);
                break;
            } else {
                b.setNonce(b.getNonce() + 1);
            }
        }
        System.out.println("Mining complete. nonce=" + b.getNonce() + " hash=" + b.getHash());
    }

    // Validate full chain (used when receiving a chain)
    public static boolean validateChain(List<Block> chainToValidate, int difficulty) {
        if (chainToValidate == null || chainToValidate.isEmpty()) return false;
        String prefixZeros = new String(new char[difficulty]).replace('\0', '0');

        // Validate genesis block exists
        // Validate each block
        for (int i = 0; i < chainToValidate.size(); i++) {
            Block current = chainToValidate.get(i);
            String calcHash = current.calculateBlockHash();
            if (!calcHash.equals(current.getHash())) {
                System.err.println("Block hash mismatch at index " + i);
                return false;
            }
            if (!current.getHash().startsWith(prefixZeros)) {
                System.err.println("Block does not meet PoW at index " + i);
                return false;
            }
            if (i > 0) {
                Block prev = chainToValidate.get(i - 1);
                if (!current.getPreviousHash().equals(prev.getHash())) {
                    System.err.println("Previous hash mismatch at index " + i);
                    return false;
                }
            }
        }
        return true;
    }

    // Validate single block against current chain (to be appended)
    private boolean validateBlock(Block b, List<Block> chainSnapshot) {
        String prefixZeros = new String(new char[mineDifficulty]).replace('\0', '0');
        // check previousHash matches last block's hash
        String lastHash = chainSnapshot.get(chainSnapshot.size() - 1).getHash();
        if (!b.getPreviousHash().equals(lastHash)) {
            System.err.println("Block previousHash doesn't match last block's hash.");
            return false;
        }
        // check hash correctness
        if (!b.calculateBlockHash().equals(b.getHash())) {
            System.err.println("Block hash invalid (calculated vs stored).");
            return false;
        }
        // pow check
        if (!b.getHash().startsWith(prefixZeros)) {
            System.err.println("Block doesn't meet proof-of-work requirement.");
            return false;
        }
        return true;
    }

    // Broadcast an object (Block or ArrayList<Block>) to all peers
    public void broadcastObject(Object obj) {
        for (PeerConnection pc : new ArrayList<>(peers.values())) {
            try {
                synchronized (pc.oos) {
                    pc.oos.writeObject(obj);
                    pc.oos.reset();
                }
            } catch (IOException e) {
                System.err.println("Error sending to peer " + pc.id + " : " + e.getMessage());
                removePeer(pc.id);
            }
        }
    }

    public void removePeer(String id) {
        PeerConnection pc = peers.remove(id);
        if (pc != null) {
            try { pc.ois.close(); } catch (Exception ignored) {}
            try { pc.oos.close(); } catch (Exception ignored) {}
            try { pc.socket.close(); } catch (Exception ignored) {}
            System.out.println("Removed peer: " + id);
        }
    }

    // Called by ReadHandler when receiving an object
    @SuppressWarnings("unchecked")
    public void handleIncoming(Object obj, PeerConnection from) {
        if (obj instanceof Block) {
            Block incoming = (Block) obj;
            synchronized (chain) {
                // If incoming block's previousHash equals our last -> validate & append
                if (incoming.getPreviousHash().equals(chain.get(chain.size() - 1).getHash())) {
                    if (validateBlock(incoming, chain)) {
                        chain.add(incoming);
                        System.out.println("Received valid block from " + from.id + " and added:");
                        System.out.println(incoming);
                        // propagate to others (except origin)
                        broadcastObject(incoming);
                    } else {
                        System.out.println("Received block failed validation from " + from.id);
                    }
                } else {
                    // If the incoming block does not chain to our last block, it might be that the sender has a longer chain.
                    // Request full chain from the peer by asking it to send its chain - in our simple protocol the peer already may sent it.
                    System.out.println("Incoming block doesn't chain to our last block. Requesting full chain or ignoring.");
                    // We will ignore the single block; however if the peer later sends a chain object, we will handle it below.
                }
            }
        } else if (obj instanceof ArrayList) {
            ArrayList<Block> incomingChain = (ArrayList<Block>) obj;
            System.out.println("Received chain from peer " + from.id + " (length=" + incomingChain.size() + ")");
            // validate incoming chain
            if (validateChain(incomingChain, mineDifficulty)) {
                synchronized (chain) {
                    // Replace our chain if incoming chain longer
                    if (incomingChain.size() > chain.size()) {
                        chain.clear();
                        chain.addAll(incomingChain);
                        System.out.println("Replaced local chain with received longer valid chain from " + from.id);
                        // broadcast the new chain to others
                        broadcastObject(new ArrayList<>(chain));
                    } else {
                        System.out.println("Received chain is valid but not longer. Ignoring.");
                    }
                }
            } else {
                System.out.println("Received chain invalid. Ignoring.");
            }
        } else {
            System.out.println("Received unknown object type from " + from.id + ": " + obj.getClass().getName());
        }
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("BCNode on port ").append(myPort).append(" chain length=").append(chain.size()).append("\n");
        synchronized (chain) {
            for (int i = 0; i < chain.size(); i++) {
                sb.append("[").append(i).append("] ").append(chain.get(i)).append("\n");
            }
        }
        sb.append("Peers:\n");
        for (String id : peers.keySet()) {
            sb.append("  ").append(id).append("\n");
        }
        return sb.toString();
    }

    // Graceful shutdown
    public void shutdown() {
        running = false;
        try { if (serverSocket != null) serverSocket.close(); } catch (Exception ignored) {}
        for (String id : new ArrayList<>(peers.keySet())) removePeer(id);
    }

    // main user loop
    public static void main(String[] args) {
        Scanner keyScan = new Scanner(System.in);
        System.out.print("Enter port to start (on current IP): ");
        int myPort = keyScan.nextInt();
        System.out.print("Enter remote ports (current IP is assumed): ");
        keyScan.nextLine();
        String line = keyScan.nextLine().trim();
        List<Integer> remotePorts = new ArrayList<>();
        if (!line.isEmpty()) {
            for (String s : line.split("\\s+")) {
                try { remotePorts.add(Integer.parseInt(s)); } catch (NumberFormatException ignored) {}
            }
        }
        System.out.print("Enter mining difficulty (e.g. 4 or 5): ");
        int difficulty = keyScan.nextInt();

        BCNode n;
        try {
            n = new BCNode(myPort, remotePorts, difficulty);
        } catch (IOException e) {
            System.err.println("Could not start node: " + e.getMessage());
            return;
        }

        String ip = "";
        try {
            ip = Inet4Address.getLocalHost().getHostAddress();
        } catch (UnknownHostException e) { /* ignore */ }

        System.out.println("Node started on " + ip + ":" + myPort);

        while (true) {
            System.out.println("\nNODE on port: " + myPort);
            System.out.println("1. Display Node's blockchain");
            System.out.println("2. Create/mine new Block");
            System.out.println("3. Kill Node");
            System.out.print("Enter option: ");
            int in = keyScan.nextInt();

            if (in == 1) {
                System.out.println(n);

            } else if (in == 2) {
                System.out.print("Enter information for new Block: ");
                String blockInfo = keyScan.next();
                Block b = new Block(blockInfo);
                n.addBlock(b);

            } else if (in == 3) {
                keyScan.close();
                n.shutdown();
                System.exit(0);
            } else {
                System.out.println("Unknown option.");
            }
        }
    }

    // package-private helpers used by ConnectionHandler / ReadHandler
    void addPeerConnection(Socket s, ObjectOutputStream oos, ObjectInputStream ois) {
        String id = s.getInetAddress().getHostAddress() + ":" + s.getPort();
        PeerConnection pc = new PeerConnection(s, oos, ois, id);
        peers.put(id, pc);
        // start a ReadHandler for this new connection
        Thread rh = new Thread(new ReadHandler(this, pc));
        rh.setDaemon(true);
        rh.start();

        // Send our chain to the new peer
        try {
            synchronized (pc.oos) {
                pc.oos.writeObject(new ArrayList<>(chain));
                pc.oos.reset();
            }
        } catch (IOException e) {
            System.err.println("Error sending chain to new peer " + id + " : " + e.getMessage());
            removePeer(id);
        }
    }
}
