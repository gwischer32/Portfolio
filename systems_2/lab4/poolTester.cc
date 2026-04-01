// poolTester.cc
#include <iostream>
#include <thread>
#include <chrono>
#include <cstdlib>
#include <string>

#include "tPool.h"

typedef struct fooParm {
    int id;
    int waitTime;
} fooParm;

void foo(void* parm) {
    fooParm* p = (fooParm*)parm; // downcast

    std::string output = "  Foo called with id " + std::to_string(p->id) + "\n";
    std::cout << output;
    std::this_thread::sleep_for(std::chrono::milliseconds(p->waitTime));
    delete p; // free the heap allocation created by addWork caller (poolTester created with new)
}

int main() {
    // deterministic randomness for testing
    srand(0);

    tPool* tp = new tPool(4);

    for (int i = 0; i < 20; i++) {
        // Slight pause before adding the next piece of work
        std::this_thread::sleep_for(std::chrono::milliseconds(rand() % 1000));

        // Ask the thread pool to do the work when it gets a chance
        // allocate the parameters on the heap (foo will delete them)
        tp->addWork(foo, new fooParm{i, rand() % 10000});
    }

    // Stop pool once all work is done
    tp->stopPool();

    delete tp;
    return 0;
}
