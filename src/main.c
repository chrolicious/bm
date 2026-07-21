#include <gbdk/platform.h>
#include <gbdk/font.h>
#include <gb/cgb.h>
#include <gb/hardware.h>
#include <gb/gb.h>
#include <stdint.h>
#include "portraits.h"
#include "bg/scenes.h"

static font_t font;

/* ── Palettes ─────────────────────────────────────────────── */

/* Single BKG palette: white bg, black text (shared by scene + text box) */
static const palette_color_t bkg_pal[4] = {
    RGB8(255, 255, 255), RGB8(170, 170, 170), RGB8( 85,  85,  85), RGB8(  0,   0,   0),
};

/* ── Sound ────────────────────────────────────────────────── */

static void sound_init(void) {
    NR52_REG = 0x80; /* sound power on */
    NR50_REG = 0x77; /* max volume, both speakers */
    NR51_REG = 0xFF; /* all channels to both outputs */
}

/* Short blip for typewriter text — Channel 2, ~880 Hz, soft */
static void sfx_blip(void) {
    NR21_REG = 0x80; /* 50% duty, no length limit */
    NR22_REG = 0x31; /* vol 3, decrease, period 1 (fast decay) */
    NR23_REG = 0x6B; /* freq low  (x = 0x76B = 1899 → ~880 Hz) */
    NR24_REG = 0x87; /* freq high 0x7 | trigger */
}

/* Item-get fanfare — Channel 2, four ascending notes (C5 E5 G5 C6) */
static void sfx_item_get(void) {
    uint8_t i;
    /* GBC freq register x: f = 131072 / (2048 - x) Hz */
    /* C5≈523Hz x=1798, E5≈659Hz x=1849, G5≈784Hz x=1881, C6≈1047Hz x=1923 */
    static const uint8_t lo[4] = {0x06, 0x39, 0x59, 0x83};
    static const uint8_t hi[4] = {0x07, 0x07, 0x07, 0x07};
    for (i = 0; i < 4; ++i) {
        NR21_REG = 0x80;
        NR22_REG = 0xF0; /* max volume, no decay */
        NR23_REG = lo[i];
        NR24_REG = hi[i] | 0x80; /* trigger */
        wait_vbl_done(); wait_vbl_done(); wait_vbl_done();
        wait_vbl_done(); wait_vbl_done(); wait_vbl_done();
        wait_vbl_done(); wait_vbl_done(); /* ~8 frames per note */
    }
    NR22_REG = 0x08; /* zero volume, stops channel */
    NR24_REG = 0x80;
}


/* ── Portraits ────────────────────────────────────────────── */
/* 7x4 OBJ grid in 8x16 mode = 56x64px; portrait starts at y=48.
   Bottom 8px (y=112-120) hidden behind text box — just feet.
   side=0 (left):  base x=0,   box open on left,  slides from left.
   side=1 (right): base x=104, box open on right, slides from right,
                   hardware X-flip (0x20) so sprite faces inward.    */

#define PORTRAIT_SCREEN_Y         48   /* 48 + 4*16 = 112 = text box top */
#define PORTRAIT_SCREEN_X_LEFT     0
#define PORTRAIT_SCREEN_X_RIGHT  104   /* 160 - 56 */
#define PORTRAIT_SPR_BASE          0

/* BKG box behind portrait: 8 cols x 9 rows.
   One border row above sprite (row 5, y=40), one border col outside sprite
   (col 7 for left box, col 12 for right box) so borders are never covered. */
#define BG_EMPTY              0   /* space tile = all-zero pixels = white under palette 0 */
#define PORTRAIT_BG_ROW       5   /* one row above sprite (y=40-47)  */
#define PORTRAIT_BG_COLS      8   /* 7 sprite cols + 1 border col    */
#define PORTRAIT_BG_ROWS      9   /* 1 top + 7 interior + 1 bottom   */
#define PORTRAIT_BG_COL_RIGHT 12  /* one col left of right portrait  */

/* Border tile indices (also defined as authoritative in text-box section) */
#define TILE_TL    95
#define TILE_TR    96
#define TILE_BL    97
#define TILE_BR    98
#define TILE_TE    99
#define TILE_BE   100
#define TILE_LE   101
#define TILE_RE   102
#define TILE_ARR  103

static const portrait_t *portrait_current    = 0;
static uint8_t           portrait_side       = 0;   /* 0=left, 1=right */
static const uint8_t    *portrait_scene_map  = 0;
static const uint8_t    *portrait_scene_attrs = 0;

static const palette_color_t spr_pal[4] = {
    RGB8(0,0,0), RGB8(255,255,255), RGB8(100,100,100), RGB8(0,0,0),
};

/* Draw or restore the 7-col x 8-row portrait box in BKG.
   Left  box: top/bottom edges + right border; left side open.
   Right box: top/bottom edges + left border;  right side open. */
static void portrait_backdrop(uint8_t show, uint8_t right) {
    uint8_t r, c;
    uint8_t row_buf[PORTRAIT_BG_COLS];
    uint8_t attr_zero[PORTRAIT_BG_COLS];
    uint8_t bkg_col = right ? PORTRAIT_BG_COL_RIGHT : 0;
    for (c = 0; c < PORTRAIT_BG_COLS; ++c) attr_zero[c] = 0;
    for (r = 0; r < PORTRAIT_BG_ROWS; ++r) {
        uint8_t tile_row = PORTRAIT_BG_ROW + r;
        if (!show) {
            if (portrait_scene_map) {
                if (portrait_scene_attrs) {
                    VBK_REG = 1;
                    set_bkg_tiles(bkg_col, tile_row, PORTRAIT_BG_COLS, 1,
                                  portrait_scene_attrs + (uint16_t)tile_row * 20 + bkg_col);
                    VBK_REG = 0;
                }
                set_bkg_tiles(bkg_col, tile_row, PORTRAIT_BG_COLS, 1,
                              portrait_scene_map + (uint16_t)tile_row * 20 + bkg_col);
            }
            continue;
        }
        if (r == 0) {
            if (right) { row_buf[0]=TILE_TL; for(c=1;c<PORTRAIT_BG_COLS;++c) row_buf[c]=TILE_TE; }
            else        { for(c=0;c<PORTRAIT_BG_COLS-1;++c) row_buf[c]=TILE_TE; row_buf[PORTRAIT_BG_COLS-1]=TILE_TR; }
        } else if (r == PORTRAIT_BG_ROWS - 1) {
            if (right) { row_buf[0]=TILE_BL; for(c=1;c<PORTRAIT_BG_COLS;++c) row_buf[c]=TILE_BE; }
            else        { for(c=0;c<PORTRAIT_BG_COLS-1;++c) row_buf[c]=TILE_BE; row_buf[PORTRAIT_BG_COLS-1]=TILE_BR; }
        } else {
            if (right) { row_buf[0]=TILE_LE; for(c=1;c<PORTRAIT_BG_COLS;++c) row_buf[c]=BG_EMPTY; }
            else        { for(c=0;c<PORTRAIT_BG_COLS-1;++c) row_buf[c]=BG_EMPTY; row_buf[PORTRAIT_BG_COLS-1]=TILE_RE; }
        }
        /* Force palette 0 (white bg) on these tiles regardless of scene attributes */
        VBK_REG = 1;
        set_bkg_tiles(bkg_col, tile_row, PORTRAIT_BG_COLS, 1, attr_zero);
        VBK_REG = 0;
        set_bkg_tiles(bkg_col, tile_row, PORTRAIT_BG_COLS, 1, row_buf);
    }
}

/* Position all portrait OBJs.  x_offset: left side [-64..0], right side [0..64].
   Right-side sprites get hardware X-flip (0x20) so they face inward.           */
static void portrait_place(int8_t x_offset, uint8_t right) {
    uint8_t i, row, col;
    int16_t obj_x;
    uint8_t base_x = right ? PORTRAIT_SCREEN_X_RIGHT : PORTRAIT_SCREEN_X_LEFT;
    uint8_t props  = right ? 0x20 : 0x00;
    i = 0;
    for (row = 0; row < PORTRAIT_SPR_ROWS; ++row) {
        for (col = 0; col < PORTRAIT_SPR_COLS; ++col) {
            obj_x = (int16_t)(base_x + col * 8 + 8) + (int16_t)x_offset;
            if (obj_x < 0)   obj_x = 0;
            if (obj_x > 255) obj_x = 255;
            move_sprite(PORTRAIT_SPR_BASE + i,
                        (uint8_t)obj_x,
                        (uint8_t)(PORTRAIT_SCREEN_Y + row * 16 + 16));
            set_sprite_prop(PORTRAIT_SPR_BASE + i, props);
            ++i;
        }
    }
}

/* Show portrait p on the given side (right=0 left, right=1 right).
   Slides old portrait out to its own side, draws new box, slides in. */
static void portrait_show(const portrait_t *p, uint8_t right) {
    uint8_t i;
    int8_t  x;

    if (p == portrait_current && right == portrait_side) return;

    if (portrait_current) {
        if (portrait_side == 0) {
            for (x=0; x>-64; x=(int8_t)(x-8)) { portrait_place(x,0); wait_vbl_done(); }
        } else {
            for (x=0; x<64;  x=(int8_t)(x+8)) { portrait_place(x,1); wait_vbl_done(); }
        }
        for (i = 0; i < PORTRAIT_N_OBJS; ++i) move_sprite(PORTRAIT_SPR_BASE + i, 0, 0);
        portrait_backdrop(0, portrait_side);
    }

    portrait_current = p;
    portrait_side    = right;
    portrait_backdrop(1, right);
    set_sprite_data(PORTRAIT_SPR_BASE, PORTRAIT_TILES, p->tiles);
    set_sprite_palette(0, 1, spr_pal);
    {
        /* For right-side portraits: X-flip each tile AND reverse column order
           so the whole portrait is a proper horizontal mirror.
           OBJ at col c gets the tile from col (SPR_COLS-1-c), then X-flipped. */
        uint8_t row, col, src_i;
        i = 0;
        for (row = 0; row < PORTRAIT_SPR_ROWS; ++row) {
            for (col = 0; col < PORTRAIT_SPR_COLS; ++col) {
                src_i = right
                    ? row * PORTRAIT_SPR_COLS + (PORTRAIT_SPR_COLS - 1u - col)
                    : i;
                move_sprite(PORTRAIT_SPR_BASE + i, 0, 0);
                set_sprite_tile(PORTRAIT_SPR_BASE + i, (uint8_t)(src_i * 2));
                set_sprite_prop(PORTRAIT_SPR_BASE + i, right ? 0x20 : 0x00);
                ++i;
            }
        }
    }

    if (right) {
        for (x=64; x>0; x=(int8_t)(x-8)) { portrait_place(x,1); wait_vbl_done(); }
        portrait_place(0, 1);
    } else {
        for (x=-64; x<0; x=(int8_t)(x+8)) { portrait_place(x,0); wait_vbl_done(); }
        portrait_place(0, 0);
    }
}

static void portrait_hide(void) {
    uint8_t i;
    int8_t  x;
    if (!portrait_current) return;
    if (portrait_side == 0) {
        for (x=0; x>-64; x=(int8_t)(x-8)) { portrait_place(x,0); wait_vbl_done(); }
    } else {
        for (x=0; x<64;  x=(int8_t)(x+8)) { portrait_place(x,1); wait_vbl_done(); }
    }
    for (i = 0; i < PORTRAIT_N_OBJS; ++i)
        move_sprite(PORTRAIT_SPR_BASE + i, 0, 0);
    portrait_backdrop(0, portrait_side);
    portrait_current = 0;
}

/* ── Text box ─────────────────────────────────────────────── */
/* Window layer: 4 tile rows at WY=112 (bottom 32px of screen).
   Layout: [border][text row 0][text row 1][border+arrow]
   Text area: tile cols 1-18 (18 chars), rows 1-2.            */

#define TB_WX    7
#define TB_WY  112
#define COLS    18
#define TROWS    2

/* font_ibm tile 0 = ASCII 32 (space), so tile index = char - 32 */
#define T(c) ((uint8_t)((uint8_t)(c) - 32u))

/* Custom border tiles at indices 95-103 (CP437 chars 127-135, never printed).
   TILE_TL/TR/BL/BR/TE/BE/LE/RE/ARR defined in portrait section above. */

/* GBC 2bpp tile data: 2 bytes per row (low plane, high plane).
   Bit 7 = leftmost pixel. color 0=white, 3=black.
   Corner tiles use a chamfered (rounded) corner pixel for the
   Pokémon Crystal look. TILE_ARR embeds the bottom-edge lines
   so the border stays intact while the arrow blinks.           */
static const uint8_t box_tiles[9 * 16] = {
    /* TILE_TL: top-left — chamfered outer pixel, 2px borders throughout */
    0x7F,0x7F, 0xFF,0xFF, 0xC0,0xC0, 0xC0,0xC0,
    0xC0,0xC0, 0xC0,0xC0, 0xC0,0xC0, 0xC0,0xC0,
    /* TILE_TR: top-right — chamfered outer pixel, 2px borders throughout */
    0xFE,0xFE, 0xFF,0xFF, 0x03,0x03, 0x03,0x03,
    0x03,0x03, 0x03,0x03, 0x03,0x03, 0x03,0x03,
    /* TILE_BL: bottom-left — 2px borders, row 6 full black where borders meet */
    0xC0,0xC0, 0xC0,0xC0, 0xC0,0xC0, 0xC0,0xC0,
    0xC0,0xC0, 0xC0,0xC0, 0xFF,0xFF, 0x7F,0x7F,
    /* TILE_BR: bottom-right — 2px borders, row 6 full black where borders meet */
    0x03,0x03, 0x03,0x03, 0x03,0x03, 0x03,0x03,
    0x03,0x03, 0x03,0x03, 0xFF,0xFF, 0xFE,0xFE,
    /* TILE_TE: top edge — 2px solid black top, white below */
    0xFF,0xFF, 0xFF,0xFF, 0x00,0x00, 0x00,0x00,
    0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00,
    /* TILE_BE: bottom edge — white above, 2px solid black bottom */
    0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00,
    0x00,0x00, 0x00,0x00, 0xFF,0xFF, 0xFF,0xFF,
    /* TILE_LE: left edge — 2px solid black left, white right */
    0xC0,0xC0, 0xC0,0xC0, 0xC0,0xC0, 0xC0,0xC0,
    0xC0,0xC0, 0xC0,0xC0, 0xC0,0xC0, 0xC0,0xC0,
    /* TILE_RE: right edge — white left, 2px solid black right */
    0x03,0x03, 0x03,0x03, 0x03,0x03, 0x03,0x03,
    0x03,0x03, 0x03,0x03, 0x03,0x03, 0x03,0x03,
    /* TILE_ARR: ▼ filled triangle + bottom-edge lines (for blink) */
    0x00,0x00, 0xFF,0xFF, 0x7E,0x7E, 0x3C,0x3C,
    0x18,0x18, 0x00,0x00, 0xFF,0xFF, 0xFF,0xFF,
};

static uint8_t tb_cx = 0;
static uint8_t tb_cy = 0;

static void tb_draw_border(void) {
    uint8_t i;
    set_win_tile_xy(0, 0, TILE_TL);
    for (i = 1; i < 19; ++i) set_win_tile_xy(i, 0, TILE_TE);
    set_win_tile_xy(19, 0, TILE_TR);
    set_win_tile_xy(0, 1, TILE_LE); set_win_tile_xy(19, 1, TILE_RE);
    set_win_tile_xy(0, 2, TILE_LE); set_win_tile_xy(19, 2, TILE_RE);
    set_win_tile_xy(0, 3, TILE_BL);
    for (i = 1; i < 19; ++i) set_win_tile_xy(i, 3, TILE_BE);
    set_win_tile_xy(19, 3, TILE_BR);
}

static void tb_clear_text(void) {
    uint8_t x, y;
    for (y = 1; y <= TROWS; ++y)
        for (x = 1; x <= COLS; ++x)
            set_win_tile_xy(x, y, T(' '));
    tb_cx = 0;
    tb_cy = 0;
}

static void tb_init(void) {
    uint8_t attr[20];
    uint8_t i;
    /* All window tiles use BKG palette 0 (white bg, black text).
       Call with h=1 per row: set_win_tiles with h>1 reads w*h bytes
       and would overread the 20-byte attr array for rows 1-3.    */
    for (i = 0; i < 20; ++i) attr[i] = 0;
    VBK_REG = 1;
    set_win_tiles(0, 0, 20, 1, attr);
    set_win_tiles(0, 1, 20, 1, attr);
    set_win_tiles(0, 2, 20, 1, attr);
    set_win_tiles(0, 3, 20, 1, attr);
    VBK_REG = 0;
    move_win(TB_WX, TB_WY);
    tb_draw_border();
    tb_clear_text();
    SHOW_WIN;
}

static void tb_wait_page(void) {
    uint8_t blink = 0;
    uint8_t counter = 0;
    while (joypad() & J_A) wait_vbl_done();
    while (!(joypad() & J_A)) {
        wait_vbl_done();
        if (++counter >= 20) {
            counter = 0;
            blink ^= 1;
            set_win_tile_xy(18, 3, blink ? TILE_ARR : TILE_BE);
        }
    }
    while (joypad() & J_A) wait_vbl_done();
    set_win_tile_xy(18, 3, TILE_BE);
    tb_clear_text();
}

static void tb_putchar(uint8_t ch) {
    if (ch == '\n' || tb_cx >= COLS) {
        tb_cx = 0;
        tb_cy++;
        if (tb_cy >= TROWS) tb_wait_page();
    }
    if (ch != '\n') {
        if (tb_cx == 0 && ch == ' ') return; /* skip leading space after wrap */
        set_win_tile_xy(1 + tb_cx, 1 + tb_cy, T(ch));
        tb_cx++;
    }
}

static void tb_print(const char *s) {
    while (*s) tb_putchar((uint8_t)*s++);
}

static void tb_print_typed(const char *s) {
    uint8_t i;
    uint8_t blip_tick = 0;
    while (*s) {
        uint8_t ch = (uint8_t)*s++;
        tb_putchar(ch);
        if (ch != '\n') {
            if (++blip_tick >= 2) { sfx_blip(); blip_tick = 0; }
            for (i = 0; i < 3; ++i) wait_vbl_done();
        }
    }
}

static void tb_flush(void) {
    if (tb_cx != 0 || tb_cy != 0) tb_wait_page();
}

/* ── Dialogue API ─────────────────────────────────────────── */

static void narrate(const char *text) {
    portrait_hide();
    tb_print(text);
    tb_flush();
}

static void dialogue(const char *speaker, const char *text) {
    const portrait_t *p = portrait_for_speaker(speaker);
    if (p) portrait_show(p, 0);
    else   portrait_hide();
    tb_print(speaker);
    tb_putchar(':');
    tb_putchar(' ');
    tb_print_typed(text);
    tb_flush();
}

static void dialogue_r(const char *speaker, const char *text) {
    const portrait_t *p = portrait_for_speaker(speaker);
    if (p) portrait_show(p, 1);
    else   portrait_hide();
    tb_print(speaker);
    tb_putchar(':');
    tb_putchar(' ');
    tb_print_typed(text);
    tb_flush();
}

static uint8_t choice(const char * const *options, uint8_t n) {
    uint8_t sel = 0;
    uint8_t prev_sel = 255;
    uint8_t joy, prev_joy;
    uint8_t i, x;
    const char *opt;
    prev_joy = joypad();
    while (1) {
        if (sel != prev_sel) {
            for (i = 0; i < n && i < TROWS; ++i) {
                for (x = 1; x <= 18; ++x) set_win_tile_xy(x, 1 + i, T(' '));
                set_win_tile_xy(1, 1 + i, (i == sel) ? T('>') : T(' '));
                opt = options[i]; x = 2;
                while (*opt && x <= 18) { set_win_tile_xy(x, 1+i, T(*opt++)); ++x; }
            }
            prev_sel = sel;
        }
        wait_vbl_done();
        joy = joypad();
        if ((joy & J_UP)   && !(prev_joy & J_UP)   && sel > 0)     --sel;
        if ((joy & J_DOWN) && !(prev_joy & J_DOWN)  && sel < n - 1) ++sel;
        if ((joy & J_A)    && !(prev_joy & J_A)) {
            while (joypad() & J_A) wait_vbl_done();
            tb_clear_text();
            return sel;
        }
        prev_joy = joy;
    }
}

/* ── Badge screen ─────────────────────────────────────────── */
/* Spinning coin badge frames: badges 4/8/9/10 from Pokemon Crystal,
   scaled 2x to 32x32 (4x4 BKG tiles), GBC 2bpp. Tile slots 120-135. */
#define BADGE_TILE_BASE 120u
static const uint8_t badge_coin_frames[4][16*16] = {
    /* frame 0 = badge_4 (full face) */
    { 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x03,0x03,0x03,0x03,0x0F,0x0C,0x0F,0x0C,
      0x3F,0x3F,0x3F,0x3F,0xFF,0xC0,0xFF,0xC0,0xC3,0x3C,0xC3,0x3C,0x0C,0xF3,0x0C,0xF3,
      0xFC,0xFC,0xFC,0xFC,0xFF,0x03,0xFF,0x03,0x3F,0xC0,0x3F,0xC0,0xFC,0x03,0xFC,0x03,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xC0,0xC0,0xC0,0xC0,0x30,0xF0,0x30,0xF0,
      0x3C,0x33,0x3C,0x33,0xF0,0xCF,0xF0,0xCF,0xF3,0xCC,0xF3,0xCC,0xFC,0xC3,0xFC,0xC3,
      0x33,0xCC,0x33,0xCC,0xCF,0x30,0xCF,0x30,0x3F,0xC0,0x3F,0xC0,0xFC,0x03,0xFC,0x03,
      0xF0,0x0F,0xF0,0x0F,0xC0,0x3F,0xC0,0x3F,0x00,0xFF,0x00,0xFF,0x03,0xFC,0x03,0xFC,
      0x0C,0xFC,0x0C,0xFC,0x33,0xCF,0x33,0xCF,0xC3,0x3F,0xC3,0x3F,0x33,0xCF,0x33,0xCF,
      0xF3,0xCC,0xF3,0xCC,0xFF,0xC0,0xFF,0xC0,0xFF,0xC0,0xFF,0xC0,0x3C,0x33,0x3C,0x33,
      0xF0,0x0F,0xF0,0x0F,0xC0,0x3F,0xC0,0x3F,0x00,0xFF,0x00,0xFF,0x03,0xFC,0x03,0xFC,
      0x0C,0xF3,0x0C,0xF3,0x33,0xCC,0x33,0xCC,0xCF,0x30,0xCF,0x30,0x3C,0xC3,0x3C,0xC3,
      0xF3,0x0F,0xF3,0x0F,0xC3,0x3F,0xC3,0x3F,0x03,0xFF,0x03,0xFF,0x0C,0xFC,0x0C,0xFC,
      0x0C,0x0F,0x0C,0x0F,0x03,0x03,0x03,0x03,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x0C,0xF3,0x0C,0xF3,0x33,0xCC,0x33,0xCC,0xC0,0xFF,0xC0,0xFF,0x3F,0x3F,0x3F,0x3F,
      0xF0,0x0F,0xF0,0x0F,0xC0,0x3F,0xC0,0x3F,0x03,0xFF,0x03,0xFF,0xFC,0xFC,0xFC,0xFC,
      0x30,0xF0,0x30,0xF0,0xC0,0xC0,0xC0,0xC0,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00 },
    /* frame 1 = badge_8 (3/4 turn) */
    { 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x03,0x03,0x03,0x03,0x0C,0x0C,0x0C,0x0C,0x30,0x3F,0x30,0x3F,
      0x00,0x00,0x00,0x00,0xC0,0xC0,0xC0,0xC0,0x30,0x30,0x30,0x30,0x0C,0x0C,0x0C,0x0C,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0xC0,0xFF,0xC0,0xFF,0xC0,0xFF,0xC0,0xFF,0xC0,0xFF,0xC0,0xFF,0xC0,0xFF,0xC0,0xFF,
      0x03,0xC3,0x03,0xC3,0x3F,0xC3,0x3F,0xC3,0x3F,0xC3,0x3F,0xC3,0x3F,0xC3,0x3F,0xC3,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0xC0,0xFF,0xC0,0xFF,0xC0,0xFF,0xC0,0xFF,0xC0,0xFF,0xC0,0xFF,0xC0,0xFF,0xC0,0xFF,
      0x3F,0xC3,0x3F,0xC3,0x3F,0xC3,0x3F,0xC3,0x3F,0xC3,0x3F,0xC3,0x03,0xFF,0x03,0xFF,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x30,0x3F,0x30,0x3F,0x0C,0x0F,0x0C,0x0F,0x03,0x03,0x03,0x03,0x00,0x00,0x00,0x00,
      0x0C,0xFC,0x0C,0xFC,0x30,0xF0,0x30,0xF0,0xC0,0xC0,0xC0,0xC0,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00 },
    /* frame 2 = badge_9 (edge-on) */
    { 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x03,0x03,0x03,0x03,0x0C,0x0C,0x0C,0x0C,0x0C,0x0C,0x0C,0x0C,
      0x00,0x00,0x00,0x00,0xC0,0xC0,0xC0,0xC0,0x30,0x30,0x30,0x30,0x30,0x30,0x30,0x30,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x0C,0x0C,0x0C,0x0C,0x0F,0x0C,0x0F,0x0C,0x0F,0x0C,0x0F,0x0C,0x0F,0x0C,0x0F,0x0C,
      0x30,0x30,0x30,0x30,0xF0,0x30,0xF0,0x30,0xF0,0x30,0xF0,0x30,0xF0,0x30,0xF0,0x30,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x0F,0x0C,0x0F,0x0C,0x0F,0x0C,0x0F,0x0C,0x0F,0x0C,0x0F,0x0C,0x0C,0x0F,0x0C,0x0F,
      0xF0,0x30,0xF0,0x30,0xF0,0x30,0xF0,0x30,0xF0,0x30,0xF0,0x30,0x30,0xF0,0x30,0xF0,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x0C,0x0F,0x0C,0x0F,0x0C,0x0F,0x0C,0x0F,0x03,0x03,0x03,0x03,0x00,0x00,0x00,0x00,
      0x30,0xF0,0x30,0xF0,0x30,0xF0,0x30,0xF0,0xC0,0xC0,0xC0,0xC0,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00 },
    /* frame 3 = badge_10 (3/4 turn other side) */
    { 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x03,0x03,0x03,0x03,0x0C,0x0C,0x0C,0x0C,0x30,0x30,0x30,0x30,
      0x00,0x00,0x00,0x00,0xC0,0xC0,0xC0,0xC0,0x30,0x30,0x30,0x30,0x0C,0xFC,0x0C,0xFC,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0xC0,0xC3,0xC0,0xC3,0xFC,0xC3,0xFC,0xC3,0xFC,0xC3,0xFC,0xC3,0xFC,0xC3,0xFC,0xC3,
      0x03,0xFF,0x03,0xFF,0x03,0xFF,0x03,0xFF,0x03,0xFF,0x03,0xFF,0x03,0xFF,0x03,0xFF,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0xFC,0xC3,0xFC,0xC3,0xFC,0xC3,0xFC,0xC3,0xFC,0xC3,0xFC,0xC3,0xC0,0xFF,0xC0,0xFF,
      0x03,0xFF,0x03,0xFF,0x03,0xFF,0x03,0xFF,0x03,0xFF,0x03,0xFF,0x03,0xFF,0x03,0xFF,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
      0x30,0x3F,0x30,0x3F,0x0C,0x0F,0x0C,0x0F,0x03,0x03,0x03,0x03,0x00,0x00,0x00,0x00,
      0x0C,0xFC,0x0C,0xFC,0x30,0xF0,0x30,0xF0,0xC0,0xC0,0xC0,0xC0,0x00,0x00,0x00,0x00,
      0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00 },
};

/* Clears BKG, draws a centred bordered box with a spinning coin badge
   animation, and shows "BEST MAN BADGE" centred in the text box.    */
static void show_badge(void) {
    static const char tbl1[] = "BEST MAN BADGE";
    static const char tbl2[] = "UNLOCKED!";
    static const uint8_t anim_seq[6] = {0, 1, 2, 3, 2, 1};
    uint8_t buf[20];
    uint8_t az[20];
    uint8_t i, x, len, pad;
    uint8_t row, col, aframe, atick;

    portrait_hide();

    for (x = 0; x < 20; ++x) { buf[x] = BG_EMPTY; az[x] = 0; }

    /* Clear BKG rows 0-13 to white with palette 0 */
    VBK_REG = 1;
    for (i = 0; i < 14; ++i) set_bkg_tiles(0, i, 20, 1, az);
    VBK_REG = 0;
    for (i = 0; i < 14; ++i) set_bkg_tiles(0, i, 20, 1, buf);

    /* Box: 14 wide (cols 3-16), rows 2-10; interior 12 wide (cols 4-15) */
    buf[0]=TILE_TL; for(x=1;x<13;++x) buf[x]=TILE_TE; buf[13]=TILE_TR;
    VBK_REG=1; set_bkg_tiles(3,2,14,1,az);  VBK_REG=0; set_bkg_tiles(3,2,14,1,buf);

    buf[0]=TILE_LE; for(x=1;x<13;++x) buf[x]=BG_EMPTY; buf[13]=TILE_RE;
    for (i = 3; i < 10; ++i) {
        VBK_REG=1; set_bkg_tiles(3,i,14,1,az); VBK_REG=0; set_bkg_tiles(3,i,14,1,buf);
    }

    buf[0]=TILE_BL; for(x=1;x<13;++x) buf[x]=TILE_BE; buf[13]=TILE_BR;
    VBK_REG=1; set_bkg_tiles(3,10,14,1,az); VBK_REG=0; set_bkg_tiles(3,10,14,1,buf);

    /* Place badge tile map: 4x4 grid centred in box interior (cols 8-11, rows 4-7) */
    for (row = 0; row < 4u; ++row)
        for (col = 0; col < 4u; ++col)
            set_bkg_tile_xy((uint8_t)(8u + col), (uint8_t)(4u + row),
                            (uint8_t)(BADGE_TILE_BASE + row * 4u + col));

    /* "BEST MAN BADGE" / "UNLOCKED!" centred in text box rows 1-2 */
    for (x = 1; x <= COLS; ++x) { set_win_tile_xy(x,1,T(' ')); set_win_tile_xy(x,2,T(' ')); }
    len = (uint8_t)(sizeof(tbl1) - 1u);
    pad = (COLS - len) / 2u;
    for (i = 0; i < len; ++i)
        set_win_tile_xy((uint8_t)(1u + pad + i), 1u, T(tbl1[i]));
    len = (uint8_t)(sizeof(tbl2) - 1u);
    pad = (COLS - len) / 2u;
    for (i = 0; i < len; ++i)
        set_win_tile_xy((uint8_t)(1u + pad + i), 2u, T(tbl2[i]));

    /* Spin until A is pressed (ping-pong: 0→1→2→3→2→1→...) */
    aframe = 0; atick = 0;
    while (joypad() & J_A) wait_vbl_done();
    for (;;) {
        wait_vbl_done();
        set_bkg_data(BADGE_TILE_BASE, 16u, badge_coin_frames[anim_seq[aframe]]);
        if (++atick >= 8u) { atick = 0; aframe = (uint8_t)((aframe + 1u) % 6u); }
        if (joypad() & J_A) break;
    }
    while (joypad() & J_A) wait_vbl_done();
    tb_clear_text();
}

/* ── Background system ────────────────────────────────────── */

/* RAM copies of current scene data — scene lives in ROM bank 2.
   All GBDK VRAM functions (set_bkg_data, set_bkg_tiles) are in bank 1,
   so they cannot be called while bank 2 is mapped.  We copy everything
   to WRAM first, then restore bank 1 before calling any GBDK function.
   set_scene_bg itself is in bank 0 (<0x4000), so its loops run safely
   while bank 2 is active. */
static uint8_t scene_tile_ram[92 * 16]; /* 1472 bytes — max scene tile size */
static uint8_t scene_map_ram[360];
static uint8_t scene_attrs_ram[360];

static void set_scene_bg(const uint8_t *tiles, uint8_t ntiles,
                          const uint8_t *map,   const uint8_t *attrs) {
    uint8_t  y;
    uint16_t i;
    uint16_t tile_bytes = (uint16_t)ntiles * 16u;

    /* Map bank 2 — scene data is accessible at 0x4000-0x7FFF.
       GBDK lib functions (bank 1, 0x4000+) are now shadowed, so we
       only use inline for-loops (bank 0 code) until we switch back. */
    SWITCH_ROM(2);

    for (i = 0u; i < tile_bytes; ++i) scene_tile_ram[i]  = tiles[i];
    for (i = 0u; i < 360u;      ++i) scene_map_ram[i]   = map[i];
    for (i = 0u; i < 360u;      ++i) scene_attrs_ram[i] = attrs[i];

    /* Restore bank 1 so GBDK library functions (set_bkg_data etc.) are reachable.
       _current_bank is zero-initialized (BSS), so saved_bank would be 0 at first
       call, restoring to bank 0 and breaking all subsequent GBDK calls. */
    SWITCH_ROM(1);

    portrait_scene_map   = scene_map_ram;
    portrait_scene_attrs = scene_attrs_ram;

    set_bkg_data(104, ntiles, scene_tile_ram);
    VBK_REG = 1;
    for (y = 0; y < 18; ++y)
        set_bkg_tiles(0, y, 20, 1, scene_attrs_ram + (uint16_t)y * 20);
    VBK_REG = 0;
    for (y = 0; y < 18; ++y)
        set_bkg_tiles(0, y, 20, 1, scene_map_ram + (uint16_t)y * 20);
    SHOW_BKG;
}

/* ── Title screen ─────────────────────────────────────────── */

/* Title uses tile_origin=0, occupying VRAM slots 0..SCENE_TITLE_NTILES-1.
   This temporarily overwrites font tiles (0-93) and border tiles (95-103).
   They are restored before returning via font_load + set_bkg_data.           */
static uint8_t title_tile_ram[SCENE_TITLE_NTILES * 16];

static void title_screen(void) {
    uint8_t  y;
    uint16_t i;
    uint8_t  joy, prev_joy;

    HIDE_WIN;

    SWITCH_ROM(3);
    for (i = 0u; i < (uint16_t)SCENE_TITLE_NTILES * 16u; ++i)
        title_tile_ram[i] = scene_title_tiles[i];
    for (i = 0u; i < 360u; ++i) scene_map_ram[i]   = scene_title_map[i];
    for (i = 0u; i < 360u; ++i) scene_attrs_ram[i] = scene_title_map_attributes[i];
    SWITCH_ROM(1);

    set_bkg_data(0, SCENE_TITLE_NTILES, title_tile_ram);
    VBK_REG = 1;
    for (y = 0; y < 18; ++y)
        set_bkg_tiles(0, y, 20, 1, scene_attrs_ram + (uint16_t)y * 20);
    VBK_REG = 0;
    for (y = 0; y < 18; ++y)
        set_bkg_tiles(0, y, 20, 1, scene_map_ram + (uint16_t)y * 20);
    SHOW_BKG;

    prev_joy = joypad();
    for (;;) {
        wait_vbl_done();
        joy = joypad();
        if ((joy & (J_A | J_START)) && !(prev_joy & (J_A | J_START))) break;
        prev_joy = joy;
    }
    while (joypad() & (J_A | J_START)) wait_vbl_done();

    /* Restore font and border tiles overwritten by title image */
    font_init();
    font = font_load(font_ibm);
    font_set(font);
    set_bkg_data(95, 9, box_tiles);
    /* Wipe leftover title tiles from VRAM slots 104-161 so they don't
       bleed into the first scene before set_scene_bg overwrites them. */
    for (i = 0u; i < 58u * 16u; ++i) title_tile_ram[i] = 0x00u;
    set_bkg_data(104, 58, title_tile_ram);
    tb_init();
}

/* ── Helpers ──────────────────────────────────────────────── */

static void delay_frames(uint8_t n) { while (n--) wait_vbl_done(); }
static void fade_out(void)          { delay_frames(30); /* TODO: CGB palette fade */ }

/* ── Scene 1: Classroom ───────────────────────────────────── */
/* TOBI prefix = 6 chars → 12 avail on line 1                 */

static void scene_1_classroom(void) {
    set_scene_bg(scene_classroom_tiles, SCENE_CLASSROOM_NTILES, scene_classroom_map, scene_classroom_map_attributes);
    narrate("COLLEGE ROLDUC.");
    narrate("HAVO 3.");
    narrate("Friday morning.");
    narrate("Michel sits front\nrow.\nDress shirt.\nNotebook out.");
    narrate("Tobi in the back,\nslumped on his\ndesk.");
    dialogue("TOBI", "ugh");
    dialogue("TOBI", "look at this nerd"); /* auto-wraps: "look at this" + "nerd" */
    dialogue("TOBI", "front row\nAGAIN?");
    dialogue("TOBI", "who wears a dress\nshirt to school"); /* auto-wraps cleanly */
    dialogue("TOBI", "spasti.");
    narrate("[Bell rings.]");
    narrate("> Walk to the door.");
}

/* ── Scene 2: Schoolyard ──────────────────────────────────── */
/* FRIETS/MICHEL prefix = 8 → avail 10; BRAMT = 7 → avail 11  */

static void scene_2_schoolyard(void) {
    set_scene_bg(scene_schoolyard_tiles, SCENE_SCHOOLYARD_NTILES, scene_schoolyard_map, scene_schoolyard_map_attributes);
    narrate("Outside the gym.\nCollege Rolduc.\nSun out.");
    narrate("Friets, BramT,\nand Tobi huddled.");
    narrate("Michel walks over.");
    dialogue("FRIETS", "bro you\nHAVE to try\nthis game");
    dialogue("BRAMT", "we just hit 60"); /* auto-wraps: "we just hit" + "60" */
    dialogue("BRAMT", "the elite\nzones are insane");
    dialogue("TOBI", "michel.");
    dialogue("TOBI", "come play\nWORLD OF WARCRAFT.");
    dialogue_r("MICHEL", "can't");
    dialogue_r("MICHEL", "I'm on\nSTAR WARS GALAXIES");
    dialogue("FRIETS", "bro");
    dialogue("BRAMT", "bro");
    dialogue("TOBI", "bro");
    dialogue("TOBI", "we'll boost you\nthrough DEADMINES"); /* auto-wraps cleanly */
    dialogue_r("MICHEL", "...what is deadmines"); /* auto-wraps: "...what is" + "deadmines" */
    narrate("He would play\nthis game for\n20 years...");
    narrate("...and counting.");
    narrate("> Walk on.");
}

/* ── Scene 5: Blackwing Lair ─────────────────────────────── */
/* ARONIAN prefix = 9 → avail 9; AERENDIL/DIVINITY = 10 → 8  */

static void scene_5_bwl(void) {
    set_scene_bg(scene_bwl_tiles, SCENE_BWL_NTILES, scene_bwl_map, scene_bwl_map_attributes);
    narrate("Months later.");
    narrate("BLACKWING LAIR.\nRed cave palette.\nDragon eggs.");
    narrate("< Bound by Blood >");
    dialogue("ARONIAN", "ok we\npull in 30 sec");
    dialogue("ARONIAN", "EVERYONE");
    dialogue("ARONIAN", "DO NOT\nWALK LEFT\nOR RIGHT");
    dialogue("ARONIAN", "stay on\nyour mark");
    dialogue("FRIETS", "lmao\nwho would do that");
    dialogue("OZORA", "xoh u\nhear that");
    dialogue_r("XOH", "ya all good");
    dialogue_r("XOH", "just gonna\nlook around");
    narrate("[You walk left.]");
    narrate("! ! !");
    dialogue("GERRIT", "ADDS");
    dialogue("TITA", "WHERE");
    dialogue("DIVINITY", "oh no");
    dialogue("AERENDIL", "by the\nLight...");
    dialogue("FRIETS", "LMAOOOO");
    dialogue("AYARO", "well that's that"); /* auto-wraps: "well that's" + "that" */
    dialogue("ARONIAN", "WHO");
    dialogue("ARONIAN", "WHO\nPULLED");
    dialogue("OZORA", "oh my god");
    dialogue("OZORA", "oh my GOD");
    dialogue("ARONIAN", "WIPE IT\nWIPE IT WIPE IT");
    narrate("* WIPE *");
    fade_out();
    dialogue("ARONIAN", "...");
    dialogue("ARONIAN", "who is\nthis guy");
    dialogue("OZORA", "uhhhh");
    dialogue("OZORA", "my friend");
    dialogue("GERRIT", "oof");
    dialogue("FRIETS", "RIP xoh");
    dialogue("ARONIAN", "hes off\nthe team");
    dialogue("ARONIAN", "demoted.\ncasual rank.");
    dialogue("TITA", "sorry xoh :(");
    dialogue("AERENDIL", "a noble\nattempt, friend");
    dialogue("DIVINITY", "...");
    dialogue("AYARO", "rough buddy");
    dialogue("OZORA", "xoh");
    dialogue("OZORA", "...");
    dialogue("OZORA", "spasti.");
    dialogue_r("XOH", "yeah ok fair");
    narrate("> Walk on.");
}

/* ── Scene 3: BramT's Living Room ────────────────────────── */

static void scene_3_living_room(void) {
    set_scene_bg(scene_living_room_tiles, SCENE_LIVING_ROOM_NTILES, scene_living_room_map, scene_living_room_map_attributes);
    narrate("BRAMT'S LIVING\nROOM. Evening.");
    narrate("BramT on the\ncouch. Benny on\nthe floor.");
    narrate("Tobi in the chair.\nGuitar by the\nwall.");
    narrate("Michel walks in.");
    dialogue("BRAMT", "Yo Mich");
    dialogue("BENNY", "sup");
    dialogue("TOBI", "play\nsomething");
    narrate("Michel picks up\nthe guitar.");
    narrate("[Trains motif...]\n[TODO: music]");
    delay_frames(120);
    dialogue("TOBI", "...");
    dialogue("TOBI", "spasti.");
    narrate("> Walk on.");
}

/* ── Scene 4: La Cubanita ────────────────────────────────── */
/* WAITRESS prefix = 10 → avail 8                             */

static void scene_4_spain(void) {
    set_scene_bg(scene_spain_bar_tiles, SCENE_SPAIN_BAR_NTILES, scene_spain_bar_map, scene_spain_bar_map_attributes);
    static const char * const r1[2] = {"YES",         "NO"          };
    static const char * const r2[2] = {"Yeah ...hic", "Nope"        };
    static const char * const r3[2] = {"Mrrghhh",     "Hnnffff"     };
    static const char * const r4[2] = {"Yshhhrrgggh", "Brbbblblbbb" };

    narrate("LA CUBANITA.\nEvening.");
    narrate("Michel and Tobi\nat a table.");
    dialogue("TOBI", "...");
    dialogue("TOBI", "they're\ndefinitely\nflirting");
    dialogue_r("MICHEL", "they're\nflirting with\nour WALLETS");
    dialogue("TOBI", "they want me");
    dialogue_r("MICHEL", "they want\nour MONEY");
    dialogue("TOBI", "spasti");
    narrate("Player walks\nto the bar.");
    dialogue("WAITRESS", "hola\nguapo");
    while (narrate("ANOTHER ROUND?"), choice(r1, 2) != 0)
        dialogue("WAITRESS", "Come on Papi,\nuno mas?");
    while (narrate("ANOTHER ROUND?"), choice(r2, 2) != 0)
        dialogue("WAITRESS", "Come on Papi,\nuno mas?");
    while (narrate("ANOTHER ROUND?"), choice(r3, 2) != 0)
        dialogue("WAITRESS", "Come on Papi,\nuno mas?");
    while (narrate("ANOTHER ROUND?"), choice(r4, 2) != 0)
        dialogue("WAITRESS", "Come on Papi,\nuno mas?");
    narrate("* BURP *");
    fade_out();
    set_scene_bg(scene_spain_bedroom_tiles, SCENE_SPAIN_BEDROOM_NTILES, scene_spain_bedroom_map, scene_spain_bedroom_map_attributes);
    narrate("BEDROOM. MORNING.");
    narrate("Tobi on the bed.\nFully horizontal.");
    dialogue("TOBI", "...");
    dialogue("TOBI", "oh no");
    narrate("[A door slams.]");
    dialogue("DAD", "TOBIAS.");
    dialogue("DAD", "MAUEL.");
    dialogue("DAD", "WAS.");
    dialogue("DAD", "ZUM.");
    dialogue("DAD", "FICK.");
    dialogue("TOBI", "spasti.");
    dialogue_r("MICHEL", "me?");
    dialogue_r("MICHEL", "you puked\non yourself");
    dialogue("TOBI", "*sigh*");
    narrate("> Walk on.");
}

/* ── Scene 6: Aachen ─────────────────────────────────────── */

static void scene_6_aachen(void) {
    set_scene_bg(scene_aachen_tiles, SCENE_AACHEN_NTILES, scene_aachen_map, scene_aachen_map_attributes);
    narrate("INSIDE THE CLUB.\nAACHEN. Late.");
    narrate("Tobi walks toward\nthe exit.\nNo words.");
    narrate("> Follow.");
    narrate("[Door closes.\nBass muffles.]");
    delay_frames(30);
    narrate("[Stairway. Night.\nTobi alone at\nthe top.]");
    delay_frames(60);
    narrate("[Michel walks up\nthe stairs.]");
    delay_frames(60);
    dialogue("TOBI", "...");
    narrate("[Tobi shakes.\nThen doesn't\nstop.]");
    delay_frames(30);
    narrate("- hug -");
    delay_frames(60);
    narrate("[Long quiet.]");
    dialogue("TOBI", "...\nthanks.");
    dialogue_r("MICHEL", "yeah.");
    delay_frames(90);
    narrate("that night\nmoved me.");
    narrate("your strength --\nto have held\nthis in all day.");
    narrate("but it also moved\nme closer to you.");
    narrate("you were my\nbrother now.");
    narrate("and i'd move\nheaven and earth\nto protect you.");
    delay_frames(30);
    dialogue("NPC", "HAH");
    dialogue("NPC", "GAY!");
    narrate("! ! !");
    dialogue_r("MICHEL", "Halt's\nMaul du Spasti.");
    narrate("[NPCs walk off.]");
    delay_frames(60);
    dialogue("TOBI", "...");
    dialogue("TOBI", "...Spastis.");
    dialogue_r("MICHEL", "yeah.");
    narrate("> Walk on.");
}

/* ── Scene 7: The Ask ────────────────────────────────────── */

static void scene_7_ask(void) {
    set_scene_bg(scene_ask_tiles, SCENE_ASK_NTILES, scene_ask_map, scene_ask_map_attributes);
    static const char * const answers[2] = {"Yes", "Heil Yes"};

    dialogue_r("MICHEL", "tobi.");
    dialogue("TOBI", "...\nmichel.");
    delay_frames(30);
    dialogue_r("MICHEL", "this whole game\nwas a question."); /* auto-wraps cleanly */
    narrate("[Trains motif\nreturns.]\n[TODO: music]");
    narrate("20+ years, tobi.");
    narrate("everything we've\nbeen through.");
    narrate("every fight.\nevery laugh.\nevery loss.");
    narrate("and somehow it\njust kept getting\ndeeper.");
    narrate("stronger.");
    narrate("every year.");
    dialogue_r("MICHEL", "will you\nbe my best man?");
    choice(answers, 2);
    sfx_item_get();
    narrate("*POOF*");
    show_badge();
}

/* ── Debug scene picker ───────────────────────────────────── */
/* Scrollable list (UP/DOWN) of all scenes; press A to launch.
   Loops so you can jump between scenes repeatedly.            */
static void debug_menu(void) {
    static const char * const names[] = {
        "1. CLASSROOM",
        "2. SCHOOLYARD",
        "3. BWL",
        "4. SPAIN BAR",
        "5. LIVING ROOM",
        "6. AACHEN",
        "7. THE ASK",
    };
    uint8_t sel, prev_sel, joy, prev_joy, x;
    const char *p;

    while (1) {
        portrait_hide();
        sel = 0; prev_sel = 255;
        prev_joy = joypad();

        while (1) {
            if (sel != prev_sel) {
                for (x = 1; x <= COLS; ++x) {
                    set_win_tile_xy(x, 1, T(' '));
                    set_win_tile_xy(x, 2, T(' '));
                }
                set_win_tile_xy(1, 1, T('>'));
                p = names[sel]; x = 2;
                while (*p && x <= COLS) { set_win_tile_xy(x, 1, T(*p++)); ++x; }
                if (sel + 1u < 7u) {
                    set_win_tile_xy(1, 2, T(' '));
                    p = names[sel + 1u]; x = 2;
                    while (*p && x <= COLS) { set_win_tile_xy(x, 2, T(*p++)); ++x; }
                }
                prev_sel = sel;
            }
            wait_vbl_done();
            joy = joypad();
            if ((joy & J_UP)   && !(prev_joy & J_UP)   && sel > 0)  --sel;
            if ((joy & J_DOWN) && !(prev_joy & J_DOWN)  && sel < 6u) ++sel;
            if ((joy & J_A)    && !(prev_joy & J_A)) {
                while (joypad() & J_A) wait_vbl_done();
                tb_clear_text();
                break;
            }
            prev_joy = joy;
        }

        fade_out();
        switch (sel) {
            case 0: scene_1_classroom();   break;
            case 1: scene_2_schoolyard();  break;
            case 2: scene_5_bwl();         break;
            case 3: scene_4_spain();       break;
            case 4: scene_3_living_room(); break;
            case 5: scene_6_aachen();      break;
            case 6: scene_7_ask();         break;
        }
    }
}

/* ── Main ────────────────────────────────────────────────── */

void main(void) {
    set_bkg_palette(0, 1, bkg_pal);
    DISPLAY_ON;
    font_init();
    font = font_load(font_ibm);
    font_set(font);
    /* Load custom tiles into VRAM:
       95-103 = border/arrow (box_tiles), 104-110 = scene backgrounds */
    VBK_REG = 0;
    set_bkg_data(95, 9, box_tiles);
    sound_init();
    /* Init all portrait sprite slots off-screen */
    {
        uint8_t i;
        SHOW_SPRITES;
        SPRITES_8x16;
        for (i = 0; i < PORTRAIT_N_OBJS; ++i)
            move_sprite(i, 0, 0);
    }
    tb_init();

    title_screen();
    debug_menu();
}
