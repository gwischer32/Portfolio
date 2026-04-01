#include <iostream>
#include <iomanip>
#include <cstdlib>

using namespace std;

int numRes;
int numProc;
int** resourceGraph;

void displayResGraph();
int deadlockCheck();
int processDFS(int p, bool visited[]);
int resourceDFS(int r, bool visited[]);
void deadlockTester();


int main() {

    // Run the deadlock test and then exit
    deadlockTester();
    exit(0);

    // Later on, you will run the dining philosophers here.
    return 0;
}

void displayResGraph() {
    cout << "\nResource Graph (process rows → resource columns):\n";
    for (int i = 0; i < numProc; i++) {
        for (int j = 0; j < numRes; j++) {
            cout << setw(3) << resourceGraph[i][j] << " ";
        }
        cout << endl;
    }
    cout << endl;
}

int processDFS(int p, bool visited[]) {

    if (visited[p]) {
        return 1; // cycle detected
    }

    visited[p] = true;

    // Search across row p for +1 edges (process -> resource)
    for (int r = 0; r < numRes; r++) {
        if (resourceGraph[p][r] == +1) {
            if (resourceDFS(r, visited) == 1)
                return 1;
        }
    }

    visited[p] = false;  // backtrack
    return 0;
}

int resourceDFS(int r, bool visited[]) {

    // Search down column r for -1 edges (resource -> process)
    for (int p = 0; p < numProc; p++) {
        if (resourceGraph[p][r] == -1) {
            if (processDFS(p, visited) == 1)
                return 1;
        }
    }

    return 0;
}

int deadlockCheck() {

    bool* visited = new bool[numProc];

    for (int p = 0; p < numProc; p++) {

        for (int i = 0; i < numProc; i++)
            visited[i] = false;

        if (processDFS(p, visited) == 1) {
            delete[] visited;
            return 1; // cycle found
        }
    }

    delete[] visited;
    return 0; // no cycles
}

// ---------------------------
// Deadlock Tester
// ---------------------------

void deadlockTester() {

    numProc = 7;
    numRes = 6;

    resourceGraph = new int*[numProc];
    for (int i = 0; i < numProc; i++) {
        resourceGraph[i] = new int[numRes];
        for (int j = 0; j < numRes; j++)
            resourceGraph[i][j] = 0;
    }

    // Hard-coded graph from the assignment
    resourceGraph[0][0] = -1;  // R->A
    resourceGraph[0][1] = +1;  // A->S

    resourceGraph[1][2] = +1;  // B->T

    resourceGraph[2][1] = +1;  // C->S

    resourceGraph[3][1] = +1;  // D->S
    resourceGraph[3][2] = +1;  // D->T
    resourceGraph[3][3] = -1;  // U->D

    resourceGraph[4][2] = -1;  // T->E
    resourceGraph[4][4] = +1;  // E->V

    resourceGraph[5][1] = +1;  // F->S
    resourceGraph[5][5] = -1;  // W->F

    resourceGraph[6][3] = +1;  // G->U
    resourceGraph[6][4] = -1;  // V->G

    displayResGraph();

    int deadlock = deadlockCheck();

    if (deadlock)
        cout << "Deadlock detected\n";
    else
        cout << "No deadlock detected\n";
}
