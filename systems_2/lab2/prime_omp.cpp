#include <iostream>
#include <cmath>
#include <omp.h>
using namespace std;

// Check if a number is prime (simple method)
bool isPrime(long n) {
    if (n < 2) return false;
    if (n == 2) return true;
    if (n % 2 == 0) return false;
    long limit = sqrt(n);
    for (long i = 3; i <= limit; i += 2) {
        if (n % i == 0) return false;
    }
    return true;
}

// BLOCKING: each thread gets a contiguous chunk
long parallel_blocking(long start, long end, int numThreads) {
    long totalPrimes = 0;

    // per-thread tracking
    long *threadCounts = new long[numThreads]();
    double *threadTimes = new double[numThreads]();

    double overallStart = omp_get_wtime();

    #pragma omp parallel num_threads(numThreads)
    {
        int tid = omp_get_thread_num();
        int NT = omp_get_num_threads();

        long range = end - start + 1;
        long chunk = range / NT;
        long myStart = start + tid * chunk;
        long myEnd = (tid == NT - 1 ? end : myStart + chunk - 1);

        double t0 = omp_get_wtime();
        long localCount = 0;

        for (long n = myStart; n <= myEnd; n++) {
            if (isPrime(n)) localCount++;
        }

        double t1 = omp_get_wtime();
        threadCounts[tid] = localCount;
        threadTimes[tid] = t1 - t0;
    }

    double overallEnd = omp_get_wtime();

    // summarize
    cout << "Blocking\n";
    long sum = 0;
    for (int i = 0; i < numThreads; i++) {
        cout << "  time for " << i << ": " 
             << threadTimes[i] << " with "
             << threadCounts[i] << " found\n";
        sum += threadCounts[i];
    }
    cout << "overall time: " << (overallEnd - overallStart)
         << " with " << sum << " found\n\n";

    delete[] threadCounts;
    delete[] threadTimes;

    return sum;
}

// STRIPING: each thread processes numbers in round-robin order
long parallel_striping(long start, long end, int numThreads) {
    long totalPrimes = 0;

    long *threadCounts = new long[numThreads]();
    double *threadTimes = new double[numThreads]();

    double overallStart = omp_get_wtime();

    #pragma omp parallel num_threads(numThreads)
    {
        int tid = omp_get_thread_num();
        int NT = omp_get_num_threads();

        double t0 = omp_get_wtime();
        long localCount = 0;

        // each thread does n = start+tid, start+tid+NT, ...
        for (long n = start + tid; n <= end; n += NT) {
            if (isPrime(n)) localCount++;
        }

        double t1 = omp_get_wtime();
        threadCounts[tid] = localCount;
        threadTimes[tid] = t1 - t0;
    }

    double overallEnd = omp_get_wtime();

    cout << "Striping\n";
    long sum = 0;
    for (int i = 0; i < numThreads; i++) {
        cout << "  time for " << i << ": " 
             << threadTimes[i] << " with "
             << threadCounts[i] << " found\n";
        sum += threadCounts[i];
    }
    cout << "overall time: " << (overallEnd - overallStart)
         << " with " << sum << " found\n\n";

    delete[] threadCounts;
    delete[] threadTimes;

    return sum;
}

// Main

int main() {
    long start = 1000;
    long end   = 1000000;
    int numThreads = 5;

    omp_set_num_threads(numThreads);

    // Run the Blocking version
    parallel_blocking(start, end, numThreads);

    // Run the Striping version
    parallel_striping(start, end, numThreads);

    return 0;
}
