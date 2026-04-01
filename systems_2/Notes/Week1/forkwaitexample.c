    #include <stdio.h>
    #include <stdlib.h>
    #include <unistd.h>
    #include <sys/wait.h>
    //#include <errno.h>
    #include <signal.h>
    void handler(int sig) {
        printf("handler called\n");
    }
    int main() {
    int foo = 5;
    signal(SIGCHLD, handler); // SIG_DFL, SIG_IGN, or handlername
    // kill(pid, SIGINT);
    int pid = fork();
    if (pid == 0) { // child
        int mypid = getpid();
        printf("child has pid of %d\n", mypid);
        // sleep for 10 seconds
        // sleep(100);
        // printf("child done sleeping\n");
        char* args[5];
        args[0] = "ps";
        // args[1] = "-l";
        args[1] = NULL;
        int rc = execvp(args[0], args);
        printf("Won't execute unless execvp fails\n");
    } 
    else {// > 0, parent - pid is the pid of the child
        printf("parent - with child pid of %d\n", pid);
        int status;
        // reaping the child
        int result = waitpid(pid, &status, 0); // blocking
        sleep(15);
        // -1 for the pid allows the parent to reap any of its children
        //int result = waitpid(-1, &status, 0); // blocking
        //int result = waitpid(-1, &status, WNOHANG); // non-blocking
        printf("parent got %d\n", result);
        sleep(10);
    }
    }
