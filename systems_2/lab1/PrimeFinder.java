public class PrimeFinder {
    // Check if number is prime or not
    public static boolean isPrime(int n) {
        if (n < 2) {
            return false;
        }
        int divisor = 2;
        boolean prime = true;

        // check divisors 2 up til n - 1
        while (divisor < n && prime) {
            if (n % divisor == 0) {
                prime = false;
            }
            divisor++;
        }
        return prime;
    }

    // Runnable function for each thread to run
    static class PrimeTask implements Runnable {
        private final int start;
        private final int end;
        private final int threadIndex;
        private final int[] results;

        public PrimeTask(int start, int end, int threadIndex, int[] results) {
            this.start = start;
            this.end = end;
            this.threadIndex = threadIndex;
            this.results = results;
        }

        @Override
        public void run() {
            System.out.println("Thread " + threadIndex +
                               " working on range [" + start + ".." + end + "]");
        
            int count = 0;
            int num = start;
            while (num <= end) {
                if (PrimeFinder.isPrime(num)) {   // ✅ fixed
                    count++;
                }
                num++;
            }
            results[threadIndex] = count;

            System.out.println("Thread " + threadIndex +
                               " finished with result = " + count);
        }
    }

    public static void main(String[] args) {
        // Easy-to-change
        int rangeStart = 100;
        int rangeEnd   = 1_000_000;
        int numThreads = 8;
        System.out.println("Counting primes in range [" +
                           rangeStart + ".." + rangeEnd + "] using " +
                           numThreads + " threads");

        int[] results = new int[numThreads];
        Thread[] threads = new Thread[numThreads];
        
        int totalNumbers = (rangeEnd - rangeStart + 1);
        int blockSize = totalNumbers / numThreads;
        long t1 = System.currentTimeMillis();

        // Launch threads
        for (int i = 0; i < numThreads; i++) {
            int start = rangeStart + i * blockSize;
            int end = (i == numThreads - 1) ? rangeEnd : (start + blockSize - 1);

            threads[i] = new Thread(new PrimeTask(start, end, i, results));
            threads[i].start();
        }

        // Wait for all threads to finish
        for (int i = 0; i < numThreads; i++) {
            try {
                threads[i].join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        // Add up results
        int totalPrimes = 0;
        for (int count : results) {
            totalPrimes += count;
        }

        long t2 = System.currentTimeMillis();
        long ms = (t2 - t1);
        double sec = ms / 1000.0;

        System.out.println("Total primes in [" + rangeStart + ".." + rangeEnd + "] = " + totalPrimes);
        System.out.println("Time taken: " + sec + " seconds (" + ms + " ms)");
    }
}
