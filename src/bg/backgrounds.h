#pragma once
#include <stdint.h>

/* Tile counts (n_tiles = array_bytes / 16) */
#define BG_CLASSROOM_N    83
#define BG_SCHOOLYARD_N   94
#define BG_BWL_N          62
#define BG_LIVING_ROOM_N  93
#define BG_SPAIN_N       121
#define BG_AACHEN_N       78
#define BG_ASK_N          94

/* All tilemaps are 16 tiles wide (128px source images).
   128x48 px -> map_h=6;  128x96 px -> map_h=12.       */
#define BG_MAP_W 16

#define BG_CLASSROOM_MAP_H    6
#define BG_SCHOOLYARD_MAP_H  12
#define BG_BWL_MAP_H          6
#define BG_LIVING_ROOM_MAP_H 12
#define BG_SPAIN_MAP_H       12
#define BG_AACHEN_MAP_H      12
#define BG_ASK_MAP_H          6

extern const uint8_t bg_classroom_tiles[];
extern const unsigned char bg_classroom_map[];
extern const unsigned char bg_classroom_map_attributes[];

extern const uint8_t bg_schoolyard_tiles[];
extern const unsigned char bg_schoolyard_map[];
extern const unsigned char bg_schoolyard_map_attributes[];

extern const uint8_t bg_bwl_tiles[];
extern const unsigned char bg_bwl_map[];
extern const unsigned char bg_bwl_map_attributes[];

extern const uint8_t bg_living_room_tiles[];
extern const unsigned char bg_living_room_map[];
extern const unsigned char bg_living_room_map_attributes[];

extern const uint8_t bg_spain_tiles[];
extern const unsigned char bg_spain_map[];
extern const unsigned char bg_spain_map_attributes[];

extern const uint8_t bg_aachen_tiles[];
extern const unsigned char bg_aachen_map[];
extern const unsigned char bg_aachen_map_attributes[];

extern const uint8_t bg_ask_tiles[];
extern const unsigned char bg_ask_map[];
extern const unsigned char bg_ask_map_attributes[];
