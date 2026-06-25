#include <gbdk/platform.h>
#include <gbdk/font.h>
#include <stdint.h>
#include <stdio.h>

/*
 * bm — best-men GBC cartridge for Tobi (handle: Ozora)
 * Engine status: minimal text-box, no backgrounds/sprites yet.
 * Scene 1 (Classroom) is wired as a proof of dialogue flow.
 */

static font_t font;

/* Wait until A is pressed and then released (debounce). */
static void wait_a(void) {
    while (!(joypad() & J_A)) wait_vbl_done();
    while (joypad() & J_A)    wait_vbl_done();
}

/* Print a block and wait for A. */
static void say(const char *text) {
    printf("%s\n", text);
    wait_a();
}

/* Scroll the screen clean by spamming newlines past the bottom. */
static void clear_screen(void) {
    uint8_t i;
    for (i = 0; i < 18; ++i) printf("\n");
}

static void scene_1_classroom(void) {
    say("COLLEGE ROLDUC.");
    say("HAVO 3.");
    say("Friday morning.");
    clear_screen();

    say("Michel sits front row.\nDress shirt. Notebook\nout.");
    clear_screen();

    say("Tobi in the back,\nslumped on his desk.");
    clear_screen();

    say("TOBI:");
    say(" ugh");
    say(" look at this nerd");
    say(" front row AGAIN?");
    say(" who wears a dress\n shirt to school");
    say(" spasti.");
    clear_screen();

    say("[Bell rings.]");
    clear_screen();

    say("> Walk to the door.");
}

void main(void) {
    DISPLAY_ON;
    font_init();
    font = font_load(font_min);
    font_set(font);

    scene_1_classroom();

    while (1) wait_vbl_done();
}
