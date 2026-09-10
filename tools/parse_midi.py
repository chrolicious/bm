"""Parse a MIDI file and print all melody notes from the lead channel."""
import struct, sys

def read_var(data, p):
    val = 0
    while True:
        b = data[p]; p += 1
        val = (val << 7) | (b & 0x7F)
        if not (b & 0x80): break
    return val, p

NOTE_NAMES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

def midi_name(n):
    return f"{NOTE_NAMES[n%12]}{(n//12)-1}"

def parse_midi(path):
    with open(path,'rb') as f:
        data = f.read()

    assert data[0:4] == b'MThd', "Not a MIDI file"
    hlen = struct.unpack('>I', data[4:8])[0]
    fmt, ntracks, ticks = struct.unpack('>HHH', data[8:14])
    print(f"Format={fmt}  Tracks={ntracks}  Ticks/quarter={ticks}")

    pos = 8 + hlen
    tempo = 500000  # 120 BPM default

    all_tracks = []

    for track_num in range(ntracks):
        assert data[pos:pos+4] == b'MTrk', f"Expected MTrk at {pos}"
        tlen = struct.unpack('>I', data[pos+4:pos+8])[0]
        pos += 8
        end = pos + tlen

        time = 0
        events = []
        last_status = 0
        p = pos

        while p < end:
            delta, p = read_var(data, p)
            time += delta

            b = data[p]
            if b & 0x80:
                last_status = b; p += 1
            else:
                b = last_status  # running status

            ev  = (last_status >> 4) & 0x0F
            ch  = last_status & 0x0F

            if ev == 0x9:   # note on
                note, vel = data[p], data[p+1]; p += 2
                if vel > 0:
                    events.append(('on', time, note, vel))
                else:
                    events.append(('off', time, note))
            elif ev == 0x8: # note off
                note = data[p]; p += 2
                events.append(('off', time, note))
            elif ev in (0xA, 0xB, 0xE):
                p += 2
            elif ev in (0xC, 0xD):
                p += 1
            elif last_status == 0xFF:  # meta
                mtype = data[p]; p += 1
                mlen, p = read_var(data, p)
                if mtype == 0x51:  # set tempo
                    tempo = int.from_bytes(data[p:p+3], 'big')
                    print(f"  Track {track_num}: Tempo={60_000_000//tempo} BPM ({tempo} us/beat)")
                p += mlen
            elif last_status == 0xF0 or last_status == 0xF7:  # sysex
                slen, p = read_var(data, p)
                p += slen
            else:
                p += 1

        all_tracks.append(events)
        pos = end

    print(f"\nTempo at parse time: {60_000_000//tempo} BPM  ({tempo} us/quarter)")
    print(f"Ticks per quarter: {ticks}")
    us_per_tick = tempo / ticks
    print(f"us per tick: {us_per_tick:.2f}")
    frames_per_tick = (60.0 / 1_000_000) * us_per_tick  # at 60fps
    print(f"frames per tick (60fps): {frames_per_tick:.4f}")

    # Print note-ons from each track
    for i, events in enumerate(all_tracks):
        note_ons = [(t, n, v) for ev, t, *rest in events
                    if ev == 'on' for n, v in [rest]]
        if not note_ons:
            continue
        print(f"\n=== Track {i} ({len(note_ons)} note-ons) ===")
        for t, n, v in note_ons[:120]:
            frames = t * frames_per_tick
            beats  = t / ticks
            print(f"  beat {beats:6.3f}  frame {frames:6.1f}  {midi_name(n):4s}  vel={v}")
        if len(note_ons) > 120:
            print(f"  ... ({len(note_ons)-120} more)")

if __name__ == '__main__':
    parse_midi(sys.argv[1])
