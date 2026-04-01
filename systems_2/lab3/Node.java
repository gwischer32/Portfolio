import java.io.*;
import java.net.*;

public class Node {

    private static final String HEAD_IP = "127.0.0.1";  // CHANGE IF RUNNING REMOTELY
    private static final int PORT = 5000;

    public static void main(String[] args) throws Exception {

        Socket sock = new Socket(HEAD_IP, PORT);
        BufferedReader in = new BufferedReader(new InputStreamReader(sock.getInputStream()));
        PrintWriter out = new PrintWriter(sock.getOutputStream(), true);

        // Wait for assigned range
        String line = in.readLine();
        String[] parts = line.split(" ");
        int start = Integer.parseInt(parts[0]);
        int end = Integer.parseInt(parts[1]);

        System.out.println("Node working on range [" + start + "..." + end + "]");

        int count = countPrimes(start, end);

        out.println(count);

        sock.close();
    }

    public static boolean isPrime(int n) {
        if (n < 2) return false;
        if (n % 2 == 0 && n != 2) return false;
        for (int i = 3; i * i <= n; i += 2)
            if (n % i == 0) return false;
        return true;
    }

    public static int countPrimes(int start, int end) {
        int c = 0;
        for (int i = start; i <= end; i++)
            if (isPrime(i)) c++;
        return c;
    }
}
