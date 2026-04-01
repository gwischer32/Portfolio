#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <limits.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>

#define INPUT_SIZE 1024
#define MAX_ARGS 64

// SIGCHLD handler to reap zombie processes
void sigchld_handler(int sig) {
    // Reap all finished child processes without blocking
    while (waitpid(-1, NULL, WNOHANG) > 0);
}

int main() {
    char input[INPUT_SIZE];
    char *args[MAX_ARGS];
    char cwd[PATH_MAX];
    int running = 1;  // shell loop flag

    // Register SIGCHLD handler
    signal(SIGCHLD, sigchld_handler);

    while (running) {
        // Display prompt with current working directory
        if (getcwd(cwd, sizeof(cwd)) != NULL) {
            printf("%s> ", cwd);
            fflush(stdout);  // ensure prompt is displayed immediately
        } else {
            perror("getcwd");
            return 1;
        }

        // Read input from user
        if (fgets(input, sizeof(input), stdin) == NULL) {
            printf("\n");
            running = 0;   // Handle Ctrl+D (EOF)
            continue;
        }

        // Remove newline at end of input
        input[strcspn(input, "\n")] = '\0';

        // Tokenize input
        int argc = 0;
        char *token = strtok(input, " ");
        while (token != NULL && argc < MAX_ARGS - 1) {
            args[argc++] = token;
            token = strtok(NULL, " ");
        }
        args[argc] = NULL; // Null-terminate argument list

        if (argc == 0) {
            continue; // Ignore empty commands
        }

        // Handle "exit"
        if (strcmp(args[0], "exit") == 0) {
            running = 0;
        }
        // Handle "cd"
        else if (strcmp(args[0], "cd") == 0) {
            const char *targetDir = NULL;

            if (argc < 2) {
                // No argument → go to $HOME
                targetDir = getenv("HOME");
                if (targetDir == NULL) {
                    fprintf(stderr, "cd: HOME not set\n");
                    continue;
                }
            } else {
                targetDir = args[1];
            }

            if (chdir(targetDir) != 0) {
                perror("cd");
            }
        }
        // Handle external commands
        else {
            char *inFile = NULL;
            char *outFile = NULL;

            // Determine if command should run in background
            int background = 0;
            if (argc > 0 && strcmp(args[argc-1], "&") == 0) {
                background = 1;
                args[argc-1] = NULL; // remove '&' from arguments
                argc--;
            }

            // Look for input/output redirection
            for (int i = 0; i < argc; i++) {
                if (args[i] == NULL) continue;
                if (strcmp(args[i], "<") == 0 && i + 1 < argc) {
                    inFile = args[i + 1];
                    args[i] = NULL;
                    args[i+1] = NULL;
                } else if (strcmp(args[i], ">") == 0 && i + 1 < argc) {
                    outFile = args[i + 1];
                    args[i] = NULL;
                    args[i+1] = NULL;
                }
            }

            pid_t pid = fork();
            if (pid < 0) {
                perror("fork");
            } else if (pid == 0) {
                // Child process → handle redirection
                if (inFile) {
                    if (freopen(inFile, "r", stdin) == NULL) {
                        perror("freopen input");
                        exit(EXIT_FAILURE);
                    }
                }
                if (outFile) {
                    if (freopen(outFile, "w", stdout) == NULL) {
                        perror("freopen output");
                        exit(EXIT_FAILURE);
                    }
                }

                // Execute command
                execvp(args[0], args);
                perror("execvp");  // only reached if execvp fails
                exit(EXIT_FAILURE);
            } else {
                // Parent process
                if (!background) {
                    // Foreground → wait for child
                    int status;
                    waitpid(pid, &status, 0);
                } else {
                    // Background → don't wait; SIGCHLD handler will reap
                    printf("[Background] PID %d started\n", pid);
                }
            }
        }
    }

    return 0;
}
