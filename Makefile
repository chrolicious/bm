# bm — best-men GBC project
# Build with: make
# Clean with: make clean

GBDK    := tools/gbdk
LCC     := $(GBDK)/bin/lcc
ROM     := build/bm.gbc

SRCS    := $(wildcard src/*.c)
OBJS    := $(SRCS:src/%.c=build/%.o)

# -Wa-l: assembly listing; -Wl-m: linker map; -Wm-yc: GBC-only; -Wm-yt0x1B: MBC5+RAM+battery
LCCFLAGS := -Wa-l -Wl-m -Wl-j -Wm-yc -Wm-yt0x1B -Wm-yoA -Wm-yn"BESTMEN"

all: $(ROM)

build:
	@mkdir -p build

build/%.o: src/%.c | build
	$(LCC) $(LCCFLAGS) -c -o $@ $<

$(ROM): $(OBJS) | build
	$(LCC) $(LCCFLAGS) -o $@ $(OBJS)

clean:
	rm -rf build

.PHONY: all clean
