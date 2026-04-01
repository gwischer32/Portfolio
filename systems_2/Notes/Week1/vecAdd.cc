// compile like: g++ -std=c++11 -pthread vecAdd.cc -o vecAdd
#include <iostream>
#include <thread>

void myRun(int n, int* a, int* b, int* c, int start, int stop) {

  //std::cout << n << " " << start << " - " << stop << "\n";
  std::string output = "Thread " + std::to_string(n) + ": " + std::to_string(start) + " - " + std::to_string(stop) + "\n";
  std::cout << output;  

  // vec add
  for (int i=start; i<stop; i++) {
    c[i] = a[i] + b[i];
  }

}


int main() {

  int n = 100;
  // Note that these need to be on the heap in order to pass
  // as parameters to threads
  // on the HEAP!!!!!!!
  int* a = (int*)malloc(n*sizeof(int));
  int* b = (int*)malloc(n*sizeof(int));
  int* c = (int*)malloc(n*sizeof(int));
  //int c[n];

  for (int i=0; i<n; i++) {
    a[i] = i;
    b[i] = i;
  }

  int numThreads = 4;
  std::thread* ths[numThreads];

  for (int i=0; i<numThreads; i++) {

    int start = (n/numThreads)*i;
    int stop = (n/numThreads)*(i+1);
    
    std::thread* th = new std::thread(myRun, i, a, b, c, start, stop);
    ths[i] = th;
  }

  for (int i=0; i<numThreads; i++) {
    ths[i]->join();
  }

  for (int i=0; i<n; i++) {
    std::cout << c[i] << "\n";
  }

}
