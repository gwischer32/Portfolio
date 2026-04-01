import java.io.Serializable;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Date;

public class Block implements Serializable {
    private static final long serialVersionUID = 1L;

    private String data;
    private long timestamp;
    private int nonce;
    private String hash;
    private String previousHash;

    public Block() {
        this("Genesis Block");
    }

    public Block(String data) {
        this.data = data;
        this.timestamp = new Date().getTime();
        this.nonce = 0;
        this.previousHash = "";
        this.hash = calculateBlockHash();
    }

    public String calculateBlockHash() {
        try {
            String instanceVarData = data + Long.toString(timestamp) + Integer.toString(nonce) + previousHash;
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hashBytes = digest.digest(instanceVarData.getBytes(StandardCharsets.UTF_8));
            StringBuilder buffer = new StringBuilder();
            for (byte b : hashBytes) {
                buffer.append(String.format("%02x", b));
            }
            return buffer.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA-256 algorithm not found", e);
        }
    }

    // Getters / Setters
    public String getData() { return data; }
    public long getTimestamp() { return timestamp; }
    public int getNonce() { return nonce; }
    public void setNonce(int nonce) { this.nonce = nonce; }
    public String getHash() { return hash; }
    public void setHash(String hash) { this.hash = hash; }
    public String getPreviousHash() { return previousHash; }
    public void setPreviousHash(String prev) { this.previousHash = prev; }

    @Override
    public String toString() {
        return "Block{" +
                "data='" + data + '\'' +
                ", timestamp=" + timestamp +
                ", nonce=" + nonce +
                ", hash='" + hash + '\'' +
                ", previousHash='" + previousHash + '\'' +
                '}';
    }
}
