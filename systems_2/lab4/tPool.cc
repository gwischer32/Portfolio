// tPool.cc
#include "tPool.h"

#include <iostream>
#include <chrono>
#include <string>
#include <cstdlib> // optionally used
#include <exception>

using namespace std::chrono;

tPool::tPool(int numThreads) {
    nThreads = numThreads;
    stopping.store(false);

    // allocate semaphores (pointer style)
    qLock = new std::counting_semaphore<1>(1);        // binary semaphore used like a mutex (initially unlocked)
    workSem = new std::counting_semaphore<1000000>(0); // no tasks available initially
    emptySem = new std::counting_semaphore<1>(1);     // queue is empty initially => token = 1
    screenLock = new std::counting_semaphore<1>(1);   // protect cout

    // allocate thread pointer array on heap as requested
    ths = new std::thread*[nThreads];

    // spawn worker threads
    for (int i = 0; i < nThreads; ++i) {
        ths[i] = new std::thread(&tPool::workerThread, this, i);
    }
}

void tPool::addWork(std::function<void(void*)> f, void* parm) {
    // Protect queue operations
    qLock->acquire();
    bool wasEmpty = funcQ.empty();

    funcQ.push(f);
    paramQ.push(parm);

    // If queue was empty and now has an item, consume the emptySem token (set empty -> not empty)
    if (wasEmpty) {
        // emptySem initial = 1 when queue empty; acquiring it makes it 0 (not-empty)
        // If some race changed it, this acquire will still behave correctly for our intended protocol.
        emptySem->acquire();
    }

    qLock->release();

    // Signal there's work to be done
    workSem->release();

    // Logging (protect std::cout)
    screenLock->acquire();
    std::cout << "-->Adding work " << std::endl;
    screenLock->release();
}

void tPool::workerThread(int workerID) {
    // Print that worker started
    screenLock->acquire();
    std::cout << "Worker " << workerID << " started" << std::endl;
    screenLock->release();

    while (true) {
        // Wait for a work token (or a wakeup from stopPool)
        workSem->acquire();

        // Protect queue access
        qLock->acquire();
        if (funcQ.empty()) {
            // No real work to do: this can happen if stopPool released tokens to wake threads
            bool shouldStop = stopping.load();
            qLock->release();

            if (shouldStop) {
                // Exiting
                screenLock->acquire();
                std::cout << "Worker " << workerID << " stopping" << std::endl;
                screenLock->release();
                break;
            } else {
                // Spurious wake or race: continue waiting for actual work
                continue;
            }
        }

        // Pop one task
        auto f = funcQ.front(); funcQ.pop();
        void* parm = paramQ.front(); paramQ.pop();

        // If queue is now empty after popping, release emptySem to indicate emptiness
        if (funcQ.empty()) {
            emptySem->release(); // set empty indicator to 1
        }

        qLock->release();

        // Logging before executing the task
        screenLock->acquire();
        std::cout << "Worker " << workerID << " about to do work" << std::endl;
        screenLock->release();

        // Execute outside of locks
        try {
            f(parm);
        } catch (const std::exception& e) {
            screenLock->acquire();
            std::cout << "Worker " << workerID << " caught exception: " << e.what() << std::endl;
            screenLock->release();
        } catch (...) {
            screenLock->acquire();
            std::cout << "Worker " << workerID << " caught unknown exception in task" << std::endl;
            screenLock->release();
        }
    } // while
}

void tPool::stopPool() {
    // Wait until the queue is empty.
    // emptySem is 1 when empty, 0 when non-empty. Trying to acquire will block until it is 1.
    emptySem->acquire();

    // Now queue is empty. Tell workers to stop.
    qLock->acquire();
    stopping.store(true);
    qLock->release();

    // Wake each worker by releasing workSem so they can check stopping flag and exit.
    for (int i = 0; i < nThreads; ++i) {
        workSem->release();
    }

    // Join and delete thread objects
    for (int i = 0; i < nThreads; ++i) {
        if (ths[i]) {
            if (ths[i]->joinable()) ths[i]->join();
            delete ths[i];
            ths[i] = nullptr;
        }
    }
    delete[] ths;
    ths = nullptr;

    // Clean up semaphores
    delete qLock; qLock = nullptr;
    delete workSem; workSem = nullptr;
    delete emptySem; emptySem = nullptr;
    delete screenLock; screenLock = nullptr;
}

tPool::~tPool() {
    // If stopPool hasn't been called, attempt to stop cleanly.
    // If threads have already been deleted (ths == nullptr), do nothing.
    if (ths != nullptr) {
        // If already stopping, stopPool will simply join; otherwise it will wait for queue to drain
        try {
            stopPool();
        } catch (...) {
            // Destructor must not throw
        }
    }
}
