#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>  // posix  compile with -pthread flag

typedef struct parm {
  int threadNum;
  int* a;
  int* b;
  int* c;
  int start;
  int stop;
} Parm;

void* myRun(void* parm) {
  Parm* theParms = (Parm*)parm;

  printf("Thread %d with range %d to %d\n", theParms->threadNum, theParms->start, theParms->stop);

  // Vec add
  for (int i=theParms->start; i<theParms->stop; i++) {
    theParms->c[i] = theParms->a[i] + theParms->b[i];
  }

  return NULL;
}

int main() {
  int n = 100;
  // creates to heap
  int* a = (int*)malloc(n * sizeof(int));
  int* b = (int*)malloc(n * sizeof(int));
  int* c = (int*)malloc(n * sizeof(int));

  for (int i=0; i<n; i++) {
    a[i] = i;
    b[i] = i;
  }

  int numThreads = 4;
  pthread_t ths[numThreads];
  for (int i=0; i<numThreads; i++) {
    int start = (n/numThreads)*i;
    int stop = (n/numThreads)*(i+1);

    Parm* p = (Parm*)malloc(1 * sizeof(Parm)); // put on the heap!
    p->threadNum = i;
    p->a = a;
    p->b = b;
    p->c = c;
    p->start = start;
    p->stop = stop;

    pthread_create(&(ths[i]), NULL, myRun, (void*)p);
  }

  //while (c[99] == 0) {}  // busy wait

  for (int i=0; i<numThreads; i++) {
    pthread_join(ths[i], NULL);  // blocking
  }

  for (int i=0;i<n; i++) {
    printf("%d\n", c[i]);
  }


}
