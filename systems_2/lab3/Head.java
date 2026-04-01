import java.io.*;
import java.net.*;
import java.util.ArrayList;

public class Head {

    private static final int PORT = 5000;
    private static final int NUM_NODES = 5;     // CHANGE THIS TO MATCH YOUR TEST
    private static final int START = 1000;
    private static final int END = 1_000_000;

    private ServerSocket server;
    private final ArrayList<NodeHandler> handlers = new ArrayList<>();
    private int totalPrimes = 0;

    public static void main(String[] args) throws Exception {
        new Head().run();
    }

    public void run() throws Exception {
        server = new ServerSocket(PORT);
        System.out.println("Head waiting on port " + PORT);

        // Phase 1 — Wait for all nodes to connect
        for (int i = 0; i < NUM_NODES; i++) {
            Socket s = server.accept();
            NodeHandler h = new NodeHandler(s, i);
            handlers.add(h);
            System.out.println("Node " + i + " connected.");
        }

        System.out.println("All nodes connected.\n");

        // Phase 2 — divide work (blocking)
        int rangeSize = (END - START + 1) / NUM_NODES;

        // Phase 3 — Launch threads to send work & wait for result
        ArrayList<Thread> threads = new ArrayList<>();

        for (int i = 0; i < handlers.size(); i++) {
            int nodeStart = START + i * rangeSize;
            int nodeEnd = (i == NUM_NODES - 1) ? END : nodeStart + rangeSize - 1;

            NodeHandler h = handlers.get(i);
            h.setRange(nodeStart, nodeEnd);

            Thread t = new Thread(() -> {
                try {
                    h.doWork();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            });

            threads.add(t);
            t.start();
        }

        // Wait for all threads to finish
        for (Thread t : threads) {
            t.join();
        }

        System.out.println("\nFINAL TOTAL PRIMES = " + totalPrimes);

        // clean shutdown
        server.close();
    }

    // synchronized total update — prevents race conditions
    public synchronized void addToTotal(int count) {
        totalPrimes += count;
    }

    class NodeHandler {
        Socket sock;
        PrintWriter out;
        BufferedReader in;
        int id;
        int start, end;

        NodeHandler(Socket s, int id) throws Exception {
            this.sock = s;
            this.id = id;
            out = new PrintWriter(sock.getOutputStream(), true);
            in = new BufferedReader(new InputStreamReader(sock.getInputStream()));
        }

        public void setRange(int s, int e) {
            this.start = s;
            this.end = e;
        }

        public void doWork() throws Exception {
            // Send range to node
            out.println(start + " " + end);

            // Wait (blocking!) for result
            String line = in.readLine();
            int count = Integer.parseInt(line);

            System.out.println("Node " + id +
                    " returned " + count +
                    " primes for range [" + start + "..." + end + "]");

            addToTotal(count);
        }
    }
}
