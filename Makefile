# bm — best-men GBC project
# Build with: make
# Clean with: make clean

GBDK    := tools/gbdk

# Windows GBDK ships lcc.exe; macOS/Linux ship bare lcc. Auto-detect,
# and allow override:  make LCC=path/to/lcc
ifeq ($(OS),Windows_NT)
LCC     ?= $(GBDK)/bin/lcc.exe
else
LCC     ?= $(GBDK)/bin/lcc
endif

ROM     := build/bm.gbc

SRCS    := $(wildcard src/*.c) $(wildcard src/bg/scene_*.c)
OBJS    := $(patsubst src/%.c,build/%.o,$(SRCS))

# -Wa-l: assembly listing; -Wl-m: linker map; -Wm-yc: GBC-only; -Wm-yt0x1B: MBC5+RAM+battery
LCCFLAGS := -Wa-l -Wl-m -Wl-j -Wm-yc -Wm-yt0x1B -Wm-yoA -Wm-yn"BESTMEN"

all: $(ROM)

build:
	@mkdir -p build

build/%.o: src/%.c | build
	$(LCC) $(LCCFLAGS) -c -o $@ $<

build/bg/%.o: src/bg/%.c | build
	@mkdir -p build/bg
	$(LCC) $(LCCFLAGS) -c -o $@ $<

$(ROM): $(OBJS) | build
	$(LCC) $(LCCFLAGS) -o $@ $(OBJS)

clean:
	rm -rf build

.PHONY: all clean
