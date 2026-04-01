#include <stdio.h>

int main() {
    char line[1024];

    // Read an entire line from stdin
    if (fgets(line, sizeof(line), stdin) != NULL) {
        printf("You typed: %s", line);
    } else {
        printf("No input!\n");
    }

    return 0;
}
