#include <iostream>
#include <chrono>
#include <vector>
#include <thread>
#include <functional>

using namespace std;

// Check if a number is prime
bool isPrime(int n) {
    if (n < 2) {
        return false;
    }

    int divisor = 2;
    bool prime = true;

    // Check divisors from 2 up to n - 1
    while (divisor < n && prime) {
        if (n % divisor == 0) {
            prime = false;
        }
        divisor++;
    }

    return prime;
}

// Function for each thread to run
void countPrimesInRange(int start, int end, int threadIndex, vector<int>& results) {
    cout << "Thread " << threadIndex
         << " working on range [" << start << ".." << end << "]" << endl;
    
    int count = 0;
    int num = start;
    while (num <= end) {
        if (isPrime(num)) {
            count++;
        }
        num++;
    }
    results[threadIndex] = count;

    cout << "Thread " << threadIndex 
         << " finished with result = " << count << endl;
}

int main() {
    // Variables that are easy to change
    int rangeStart = 100;
    int rangeEnd   = 1000000;
    int numThreads = 4;

    cout << "Counting primes in range [" << rangeStart << ".." << rangeEnd << "]" 
         << " using " << numThreads << " threads" << endl;

    // Prepare results array, one slot per thread
    vector<int> results(numThreads, 0);
    vector<thread> threads;

    // Compute block size for each thread
    int totalNumbers = (rangeEnd - rangeStart + 1);
    int blockSize = totalNumbers / numThreads;

    auto t1 = chrono::high_resolution_clock::now();

    // Launch threads
    for (int i = 0; i < numThreads; i++) {
        int start = rangeStart + i * blockSize;
        int end = (i == numThreads - 1) ? rangeEnd : (start + blockSize - 1);

        threads.push_back(thread(countPrimesInRange, start, end, i, ref(results)));
    }

    // Join threads (wait for all to finish)
    for (auto& th : threads) {
        th.join();
    }

    // Add up results
    int totalPrimes = 0;
    for (int val : results) {
        totalPrimes += val;
    }

    auto t2 = chrono::high_resolution_clock::now();

    cout << "Total primes in [" << rangeStart << ".." << rangeEnd << "] = " 
         << totalPrimes << endl;

    cout << "Time taken: " 
         << chrono::duration_cast<chrono::milliseconds>(t2 - t1).count() 
         << " ms" << endl;

    return 0;
}
