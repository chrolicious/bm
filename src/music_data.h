#pragma once
#include <stdint.h>

#define MUSIC_BANK 4

/* ── Music engine ─────────────────────────────────────────── */
/* Monophonic melody on Channel 1 (NR1x), VBL-driven.
   Channel 2 (NR2x) is reserved for SFX (sfx_blip / sfx_item_get). */

typedef struct { uint8_t lo; uint8_t hi; uint16_t dur; } MNote;
#define MN(x,d) { (uint8_t)((x)&0xFFu), (uint8_t)((x)>>8u), (d) }
#define MR(d)   { 0u, 0u, (d) }
#define MLEN(a) ((uint16_t)(sizeof(a)/sizeof((a)[0])))

/* Channel 4 (noise) drums: env=NR42 (vol<<4|dir<<3|pace), poly=NR43.
   NR43: hi-nibble=clock-shift, bit3=7-bit-LFSR(1=noisy), lo3=divisor. */
typedef struct { uint8_t env; uint8_t poly; uint8_t dur; } DNote;
#define DK(d) { 0xF2u, 0xA0u, (d) }  /* kick   — deep low rumble  */
#define DS(d) { 0xF3u, 0x57u, (d) }  /* snare  — sharp crack      */
#define DH(d) { 0x72u, 0x20u, (d) }  /* hi-hat — fast click       */
#define DC(d) { 0x62u, 0x27u, (d) }  /* open cymbal               */
#define DR(d) { 0u,    0u,    (d) }  /* drum rest                 */
#define DLEN(a) ((uint16_t)(sizeof(a)/sizeof((a)[0])))

/* x = 2048 - round(131072 / Hz) */
#define F_C3   1046u
#define F_CS3  1102u
#define F_D3   1155u
#define F_DS3  1205u
#define F_E3   1253u
#define F_F3   1297u
#define F_FS3  1339u
#define F_GS3  1417u
#define F_G3   1379u
#define F_A3   1452u
#define F_AS3  1473u
#define F_BB3  1486u
#define F_B3   1517u
#define F_C4   1547u
#define F_CS4  1575u
#define F_D4   1601u
#define F_DS4  1627u
#define F_E4   1650u
#define F_F4   1673u
#define F_FS4  1694u
#define F_G4   1714u
#define F_GS4  1732u
#define F_A4   1750u
#define F_AS4  1764u
#define F_BB4  1767u
#define F_B4   1783u
#define F_C5   1797u
#define F_CS5  1811u
#define F_D5   1825u
#define F_DS5  1837u
#define F_E5   1849u
#define F_F5   1860u
#define F_FS5  1871u
#define F_G5   1881u
#define F_GS5  1890u
#define F_A5   1899u

/* Stubs — awaiting new arrangements */
extern const MNote music_trains_ch1[24];
extern const MNote music_trains_ch2[24];
extern const MNote music_trains_ch3[24];
extern const MNote music_elwynn[1];
extern const MNote music_tavern[1];
extern const MNote music_battle_ch1[94];
extern const MNote music_battle_ch2[85];
extern const MNote music_battle_ch3[218];
extern const MNote music_aachen[1];
extern const MNote music_ecruteak_ch1[10];
extern const MNote music_ecruteak_ch2[19];
extern const MNote music_ecruteak_ch3[18];
extern const MNote music_title_track_ch1[12];
extern const MNote music_title_track_ch2[12];
extern const MNote music_title_track_ch3[20];
extern const DNote drum_trains[1];
extern const DNote drum_battle[1];
extern const DNote drum_aachen[1];
extern const DNote drum_tavern[1];

/* Active arrangements */
extern const MNote music_classroom_ch1[1022];
extern const MNote music_classroom_ch3[571];
extern const MNote music_bedroom_ch1[1];
extern const MNote music_bedroom_ch2[1];
extern const MNote music_bedroom_ch3[1];
extern const MNote music_bwl_wipe_ch1[1];
extern const MNote music_bwl_wipe_ch2[1];
extern const MNote music_bwl_wipe_ch3[1];
