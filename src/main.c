#include <gbdk/platform.h>
#include <gbdk/font.h>
#include <gb/cgb.h>
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

/* Print narration instantly and wait for A. */
static void say(const char *text) {
    printf("%s\n", text);
    wait_a();
}

/* Print dialogue with typewriter effect, then wait for A. */
static void say_typed(const char *text) {
    const char *p = text;
    uint8_t i;
    while (*p) {
        putchar(*p);
        if (*p != '\n') {
            for (i = 0; i < 3; ++i) wait_vbl_done();
        }
        p++;
    }
    putchar('\n');
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

    say("Michel sits front\nrow.\nDress shirt.\nNotebook out.");
    clear_screen();

    say("Tobi in the back,\nslumped on his desk.");
    clear_screen();

    say_typed("TOBI: ugh");
    say_typed("TOBI: look at this\nnerd");
    say_typed("TOBI: front row\nAGAIN?");
    say_typed("TOBI: who wears a\ndress shirt to\nschool");
    say_typed("TOBI: spasti.");
    clear_screen();

    say("[Bell rings.]");
    clear_screen();

    say("> Walk to the door.");
}

/* White background, black text — CGB background palette 0. */
static const palette_color_t bkg_pal[4] = {
    RGB8(255, 255, 255),
    RGB8(170, 170, 170),
    RGB8( 85,  85,  85),
    RGB8(  0,   0,   0),
};

void main(void) {
    set_bkg_palette(0, 1, bkg_pal);
    DISPLAY_ON;
    font_init();
    font = font_load(font_ibm);
    font_set(font);

    scene_1_classroom();

    while (1) wait_vbl_done();
}
