#pragma once
#include <stdint.h>

/* 7x4 OBJ grid (8x16 sprite mode) = 56x56px native */
#define PORTRAIT_SPR_COLS  7
#define PORTRAIT_SPR_ROWS  4
#define PORTRAIT_N_OBJS    28
#define PORTRAIT_TILES     56

typedef struct {
    const uint8_t *tiles;  /* 56*16 bytes, GBC 2bpp */
} portrait_t;

extern const portrait_t portrait_michel;
extern const portrait_t portrait_tobi;
extern const portrait_t portrait_friets;
extern const portrait_t portrait_dad;
extern const portrait_t portrait_teacher;
extern const portrait_t portrait_waitress;
extern const portrait_t portrait_aronian;
extern const portrait_t portrait_bramt;
extern const portrait_t portrait_npc;
extern const portrait_t portrait_gerrit;
extern const portrait_t portrait_tita;
extern const portrait_t portrait_divinity;
extern const portrait_t portrait_aerendil;

const portrait_t *portrait_for_speaker(const char *name);
