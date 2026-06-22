#include <gb/gb.h>
#include <stdio.h>

void main(void) {
    DISPLAY_ON;
    printf("BESTMEN v0\n\nbuild OK");
    while (1) {
        wait_vbl_done();
    }
}
