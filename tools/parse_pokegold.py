#!/usr/bin/env python3
"""
parse_pokegold.py - Convert pret/pokegold .asm music to MNote C arrays.

Usage:
    python tools/parse_pokegold.py <track_name> <array_prefix> [loop_repeats]

    track_name  : pokegold track basename, e.g. 'johtowildbattle'
                  or a local .asm file path
    array_prefix: prefix for C arrays, e.g. 'music_battle'
                  → produces music_battle_ch1/ch2/ch3

    loop_repeats: how many times to play the main infinite loop body (default 4)

Examples:
    python tools/parse_pokegold.py johtowildbattle music_battle
    python tools/parse_pokegold.py titlescreen music_bedroom 3
"""

import sys, re, subprocess, base64

NOTE_SEMI = {
    'C_': 0, 'C#': 1, 'D_': 2, 'D#': 3, 'E_': 4, 'F_': 5,
    'F#': 6, 'G_': 7, 'G#': 8, 'A_': 9, 'A#': 10, 'B_': 11,
}

def note_freq(note_name, octave):
    # pokegold octave N = scientific octave N+1
    # (oct3 C_ -> C4 middle C; oct4 C_ -> C5)
    # Use A4=440Hz reference for precision
    semi = NOTE_SEMI[note_name]
    semitones_from_a4 = semi - 9 + (octave - 3) * 12
    hz = 440.0 * (2.0 ** (semitones_from_a4 / 12.0))
    x = int(round(2048 - 131072.0 / hz))
    return max(0, min(2047, x))

def note_frames(note_type, note_dur, tempo):
    frames = (note_type * note_dur * tempo) >> 8
    return max(1, frames)

# ---------------------------------------------------------------------------
# Fetch from GitHub
# ---------------------------------------------------------------------------

def fetch_asm(track_name):
    if not track_name.startswith('gh:') and track_name.endswith('.asm'):
        with open(track_name) as f:
            return f.read()
    basename = track_name.removeprefix('gh:').removesuffix('.asm')
    path = f'audio/music/{basename}.asm'
    result = subprocess.run(
        ['gh', 'api', f'repos/pret/pokegold/contents/{path}', '--jq', '.content'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        sys.exit(f'gh api failed: {result.stderr.strip()}')
    b64 = result.stdout.strip().replace('\n', '').replace(' ', '')
    return base64.b64decode(b64).decode('utf-8', errors='replace')

# ---------------------------------------------------------------------------
# Tokenise into (label, cmd, args) triples
# ---------------------------------------------------------------------------

def tokenize(text):
    tokens = []
    for raw_line in text.splitlines():
        line = raw_line.split(';')[0].strip()
        if not line:
            continue
        # strip label if present
        m = re.match(r'^([\w.]+):(.*)', line)
        if m:
            tokens.append((m.group(1), '__label__', []))
            line = m.group(2).strip()
            if not line:
                continue
        parts = [p for p in re.split(r'[\s,]+', line) if p]
        if parts:
            tokens.append((None, parts[0], parts[1:]))
    return tokens

def build_label_map(tokens):
    m = {}
    for i, (lbl, cmd, args) in enumerate(tokens):
        if lbl:
            m[lbl] = i
    return m

def build_scoped_label_map(tokens, start_label, global_lmap):
    """Build a label map restricted to one channel's section.

    Local labels (starting with '.') are re-scoped to only cover the tokens
    from start_label up to the next global (non-dot) label that isn't
    start_label itself.  This prevents .mainloop in Ch1 from colliding with
    .mainloop in Ch2/Ch3.
    """
    start_idx = global_lmap.get(start_label)
    if start_idx is None:
        return global_lmap

    # Find where this channel ends: the next non-dot label after start_idx
    end_idx = len(tokens)
    for i in range(start_idx + 1, len(tokens)):
        lbl, cmd, _ = tokens[i]
        if lbl and not lbl.startswith('.'):
            end_idx = i
            break

    # Build a fresh map for labels within [start_idx, end_idx)
    scoped = {}
    for i in range(start_idx, end_idx):
        lbl, cmd, _ = tokens[i]
        if lbl:
            scoped[lbl] = i
    return scoped

# ---------------------------------------------------------------------------
# Channel player — walks tokens, emits (freq, frames) pairs
# ---------------------------------------------------------------------------

class Player:
    def __init__(self, tokens, label_map, loop_repeats):
        self.tokens   = tokens
        self.lmap     = label_map
        self.repeats  = loop_repeats
        self.notes    = []
        # playback state
        self.octave    = 4
        self.note_type = 12
        self.tempo     = 256   # default: frames = note_type * dur

    # -- note emission -------------------------------------------------------

    def emit(self, freq, dur_val):
        self.notes.append((freq, note_frames(self.note_type, dur_val, self.tempo)))

    def emit_rest(self, dur_val):
        self.notes.append((0, note_frames(self.note_type, dur_val, self.tempo)))

    # -- token dispatch ------------------------------------------------------

    def apply(self, cmd, args):
        """Apply a single non-flow-control command."""
        if cmd in ('__label__', 'channel_count', 'channel',
                   'duty_cycle', 'vibrato', 'pitch_offset',
                   'volume_envelope', 'volume', 'pitch_sweep',
                   'duty_cycle_pattern', 'toggle_sfx', 'toggle_noise',
                   'force_stereo_panning', 'stereo_panning'):
            return
        if cmd == 'tempo':
            self.tempo = int(args[0])
        elif cmd == 'note_type':
            self.note_type = int(args[0])
        elif cmd == 'octave':
            self.octave = int(args[0])
        elif cmd == 'note':
            name, dur = args[0], int(args[1])
            if name in NOTE_SEMI:
                self.emit(note_freq(name, self.octave), dur)
            else:
                self.emit_rest(dur)
        elif cmd == 'rest':
            self.emit_rest(int(args[0]))

    # -- run from a label, stopping at sound_ret or end-of-stream -----------

    def run_segment(self, start_label, stop_at_ret=False, max_iter=500000):
        if start_label not in self.lmap:
            return
        pc = self.lmap[start_label]
        iterations = 0
        # loop_stack: list of (loop_start_pc, remaining_count)
        loop_stack = []

        while pc < len(self.tokens) and iterations < max_iter:
            iterations += 1
            lbl, cmd, args = self.tokens[pc]
            pc += 1

            if cmd == 'sound_ret':
                if stop_at_ret:
                    return
                break

            if cmd == 'sound_call':
                target = args[0]
                if target in self.lmap:
                    saved = pc
                    self.run_segment(target, stop_at_ret=True)
                    pc = saved
                continue

            if cmd == 'sound_loop':
                count = int(args[0])
                target = args[1]
                if target not in self.lmap:
                    continue
                loop_pc = self.lmap[target]
                if count == 0:
                    # infinite: already ran body once, run (repeats-1) more times
                    for _ in range(self.repeats - 1):
                        self.run_loop_body(loop_pc, pc - 1)
                    break  # stop after infinite loop
                else:
                    # finite: body already ran once, run (count-1) more times
                    for _ in range(count - 1):
                        self.run_loop_body(loop_pc, pc - 1)
                continue

            self.apply(cmd, args)

    def run_loop_body(self, start_pc, stop_pc):
        """Run tokens[start_pc .. stop_pc) as a loop body repetition."""
        pc = start_pc
        while pc < stop_pc and pc < len(self.tokens):
            lbl, cmd, args = self.tokens[pc]
            pc += 1
            if cmd == 'sound_call':
                target = args[0]
                if target in self.lmap:
                    saved = pc
                    self.run_segment(target, stop_at_ret=True)
                    pc = saved
                continue
            if cmd == 'sound_loop':
                # nested loop inside this body
                count = int(args[0])
                target = args[1]
                if target not in self.lmap:
                    continue
                inner_start = self.lmap[target]
                inner_end = pc - 1  # the sound_loop token position
                if count == 0:
                    count = 2  # treat nested infinite as 2 repeats
                else:
                    pass  # body already ran once (first pass)
                for _ in range(count - 1):
                    self.run_loop_body(inner_start, inner_end)
                continue
            self.apply(cmd, args)

# ---------------------------------------------------------------------------
# Parse track → {ch_num: [(freq, frames), ...]}
# ---------------------------------------------------------------------------

def parse_track(asm_text, loop_repeats):
    tokens   = tokenize(asm_text)
    lmap     = build_label_map(tokens)

    # Extract channel labels from header
    ch_labels = {}
    for lbl, cmd, args in tokens:
        if cmd == 'channel' and len(args) >= 2:
            ch_num = int(args[0])
            ch_labels[ch_num] = args[1]

    if not ch_labels:
        sys.exit('No channel directives found')

    # Find global tempo: pokegold 'tempo' sets all channels simultaneously.
    # Scan all tokens and take the first tempo command found anywhere.
    global_tempo = 256
    for lbl, cmd, args in tokens:
        if cmd == 'tempo' and args:
            global_tempo = int(args[0])
            break
    print(f'  global tempo: {global_tempo}', file=sys.stderr)

    results = {}
    for ch_num in sorted(ch_labels):
        if ch_num > 3:
            continue  # skip noise channel 4
        label  = ch_labels[ch_num]
        scoped = build_scoped_label_map(tokens, label, lmap)

        # Prefer starting from .mainloop if it exists in this channel's scope.
        # The body/intro of each channel has a different length, which would
        # shift the channels out of phase relative to each other when they loop.
        # Starting from .mainloop ensures all three channels are always in sync.
        start = '.mainloop' if '.mainloop' in scoped else label

        player = Player(tokens, scoped, loop_repeats)
        player.tempo = global_tempo
        player.run_segment(start, stop_at_ret=False)
        results[ch_num] = player.notes
        total_f = sum(f for _, f in player.notes)
        print(f'  ch{ch_num} ({label}→{start}): {len(player.notes)} notes, {total_f} frames ({total_f/60:.1f}s)', file=sys.stderr)

    # Pad shorter channels with rests so all channels loop in sync.
    # Each channel loops independently in our engine, so they must have
    # the same total frame count to stay in sync.
    max_frames = max(sum(f for _, f in notes) for notes in results.values())
    for ch_num, notes in results.items():
        total = sum(f for _, f in notes)
        diff  = max_frames - total
        if diff > 0:
            print(f'  ch{ch_num}: padding {diff} frames to sync with longest channel', file=sys.stderr)
            notes.append((0, diff))

    return results

# ---------------------------------------------------------------------------
# C output
# ---------------------------------------------------------------------------

def emit_c(channels, prefix):
    lines = []
    for ch_num, notes in sorted(channels.items()):
        arr_name = f'{prefix}_ch{ch_num}'
        count    = len(notes)
        lines.append(f'const MNote {arr_name}[{count}] = {{')
        for i, (freq, frames) in enumerate(notes):
            comma = '' if i == count - 1 else ','
            if freq == 0:
                lines.append(f'    MR({frames}){comma}')
            else:
                lo = freq & 0xFF
                hi = (freq >> 8) & 0xFF
                lines.append(f'    {{ 0x{lo:02x}u, 0x{hi:02x}u, {frames}u }}{comma}')
        lines.append('};')
        lines.append('')
    return '\n'.join(lines)

def emit_h_decls(channels, prefix):
    lines = []
    for ch_num, notes in sorted(channels.items()):
        arr_name = f'{prefix}_ch{ch_num}'
        count    = len(notes)
        lines.append(f'extern const MNote {arr_name}[{count}];')
    return '\n'.join(lines)

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)

    track_name   = sys.argv[1]
    prefix       = sys.argv[2]
    loop_repeats = int(sys.argv[3]) if len(sys.argv) > 3 else 4

    print(f'Fetching {track_name}...', file=sys.stderr)
    asm_text = fetch_asm(track_name)
    print(f'Parsing (loop_repeats={loop_repeats})...', file=sys.stderr)
    channels = parse_track(asm_text, loop_repeats)

    total = sum(len(v) for v in channels.values())
    print(f'Total notes: {total}', file=sys.stderr)

    import io, os
    out = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    out.write('/* -- Header declarations -- */\n')
    out.write(emit_h_decls(channels, prefix) + '\n\n')
    out.write('/* -- Array data -- */\n')
    out.write(emit_c(channels, prefix) + '\n')
    out.flush()
