// tPool.h
#ifndef TPOOL_H
#define TPOOL_H

#include <functional>
#include <thread>
#include <queue>
#include <semaphore>
#include <atomic>

class tPool {
public:
    // Create a pool with numThreads worker threads
    tPool(int numThreads);

    // Add a task: function that takes void* and a parameter pointer
    void addWork(std::function<void(void*)> f, void* parm);

    // Block until queued work is finished, then stop workers and join them
    void stopPool();

    // Destructor will attempt to stop the pool if not already stopped
    ~tPool();

private:
    // Main loop for each worker thread
    void workerThread(int workerID);

    // number of threads in pool
    int nThreads;

    // semaphores (allocated as pointers per lab instructions)
    // Use counting_semaphore<1> as a binary semaphore workaround for older compilers
    std::counting_semaphore<1>* qLock;               // protects queue access (binary semaphore)
    std::counting_semaphore<1000000>* workSem;      // counts available work items (counting semaphore)
    std::counting_semaphore<1>* emptySem;           // 1 when queue is empty, 0 otherwise (binary)
    std::counting_semaphore<1>* screenLock;         // protects std::cout

    // thread pointers array (allocated on heap)
    std::thread** ths;

    // work queues: functions and their parameters
    std::queue<std::function<void(void*)>> funcQ;
    std::queue<void*> paramQ;

    // flag to tell workers to exit
    std::atomic<bool> stopping;
};

#endif // TPOOL_H
