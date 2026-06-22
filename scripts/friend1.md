# Friend 1 — Tobi (Tobias)

Status: raw extraction, scene order drafted, dialogue not yet written.

## Premise

A bootleg Pokémon-style GBC "game" Michel is giving Tobi to ask him to be his best man. Player is Michel-as-trainer, walks through a small overworld where each "room" is a memory with Tobi. Ends with the ask.

**Setting:** Kerkrade, Netherlands. School = **College Rolduc**, HAVO track, klas 3 (third year). Michel commutes back to Meerbusch (Germany) on weekends to see his girlfriend **Constanze / "Conzi."** The Netherlands → Germany border-crossing weekend ritual is the unspoken context for the dress-shirt mystery.

## Characters

- **Michel** (player sprite) — proxy = `gfx/player/chris.png` (Crystal protag, recolor TBD)
- **Tobi** — needs custom sprite (Gen-2 NPC style; tall-ish, hair color TBD). Possible NPC sprite reuse for prototype: `gfx/sprites/biker.png` or `gfx/sprites/cal.png` until custom art lands.

## Voice / tone

- Mixed. Comedy bits land hard, emotional bits land harder. Crystal-era Pokémon dialogue cadence (short lines, "...", `\n` line breaks, occasional ALL CAPS for emphasis).
- Speaker tag and in-dialogue name both: **TOBI** / **Tobi**.
- It's German-speaking teen banter on the Dutch border. Mostly English, but the in-jokes drop into German: **"spasti"** is the recurring affectionate insult between them. Use it as the punchline word — not a constant tic.

## Dialogue format

Every dialogue block in this doc maps to one Pokémon-style text box. Box is ~18 chars wide × 2 lines visible at once; a third line scrolls in. We'll use this format and let the engine paginate:

```
TOBI: line one (≤18 chars)
      line two (≤18 chars)
      [▼]
      line three
```

`[▼]` = "press A to continue" marker. `...` carries weight — leave it on its own line.

## Arc

Pokémon "town" structure: 5 rooms / memories, arranged as a short overworld walk. The walk itself is the spine — each door is a year of their lives. Pacing: 3 short scenes → 1 silent beat → 1 devastating scene → the ask. Comedy carries the player through the early stuff so the Aachen scene lands.

```
[TITLE] → [CLASSROOM] → [SCHOOLYARD] → [LIVING ROOM] → [SPAIN BAR] → [AACHEN STAIRS] → [BWL RAID] → [ASK]
           cold open    WoW first hint   "trains" beat   comedy beat   climax              comedy↺      the question
```

Seven scenes. The BWL raid sits *after* Aachen on purpose: life kept going. Tobi's mom is gone, the friendship deepened, and now you're two guys laughing on Ventrilo because Michel just wiped a 40-man raid. Heartbreak → recovery → resolution.

---

## Scene 1 — Classroom (cold open, ~age 16)

**Setting:** A Pokémon Gen-2-style schoolroom interior. Desks in rows. Michel-sprite sits front-row in a dress shirt. Tobi-sprite in the back.

**Asset notes:** reuse `gfx/tilesets/elms_lab.png` palette-swapped, or `gfx/tilesets/players_room.png` repurposed; Michel-sprite = `gfx/player/chris.png` with dress-shirt palette; Tobi = placeholder NPC sprite for prototype.

**Draft dialogue (first pass, GBC-text-box sized):**

```
[COLLEGE ROLDUC. HAVO 3.
 Friday morning. Repeat year.]

[Michel-sprite sits front row.
Dress shirt. Notebook out.]

[Tobi-sprite in the back,
slumped on his desk.]

TOBI:     ugh
          [▼]
          look at this nerd
          [▼]
          front row AGAIN?
          [▼]
          who wears a dress
          shirt to school
          [▼]
          spasti.

[Bell rings.]

[NARRATOR: ▼ Walk to the door.]
```

**Notes on this draft:**
- All Tobi, no narrator confession. The "repeat year" lives in the caption header, not in Michel's inner voice. Player gets the setup in one line and moves on.
- "ugh / look at this nerd / front row AGAIN?" is the actual cadence of a 16-year-old slumped at the back. Light, dismissive, fun.
- The Meerbusch dress-shirt mystery still plants here (Tobi wonders why the shirt) — pays off in Scene 7 ("Conzi. That was Conzi.")
- "Spasti." is still the closer, but now it's a teen mutter, not a Shakespearean pronouncement.

---

## Scene 2 — Schoolyard, in front of the gym (~age 16–17)

**Setting:** Outdoor schoolyard tile, College Rolduc gym building in the background. **Friets, Bram, and Tobi** huddled, talking loud. Michel-sprite walks over.

**Asset notes:** Reuse `gfx/tilesets/johto.png` for outdoor ground. Three named NPC sprites for Friets, Bram, Tobi (pick distinct-silhouette sprites from `gfx/sprites/` — distinguishable at a glance matters since these three recur).

**Draft dialogue:**

```
[Outside the gym at College
Rolduc. Sun out.]

[Friets, Bram, and Tobi
huddled, talking loud.]

[Michel-sprite walks over.]

FRIETS:    bro you HAVE to
           try this game

BRAM:      we just hit 60
           [▼]
           the elite zones are
           insane

TOBI:      michel.
           [▼]
           come play WORLD OF
           WARCRAFT.

MICHEL:    can't
           [▼]
           I'm grinding on
           STAR WARS GALAXIES

FRIETS:    bro

BRAM:      bro

TOBI:      bro
           [▼]
           we'll boost you
           through DEADMINES

MICHEL:    ...what is deadmines

TOBI:      it's a dungeon.
           [▼]
           one dungeon.

MICHEL:    ...ok one dungeon.

[NARRATOR: He would play this
game for the next 20 years.]
[NARRATOR: ▼ Walk on.]
```

**Notes:**
- "bro / bro / bro" — teen-friend peer pressure in pure form. Three NPCs, one syllable each, then Tobi closes the deal. Reads instantly.
- "Spasti." is *absent* this scene. Tobi doesn't need it — peer pressure is enough. Saves the word for the next two scenes where it lands harder.
- STAR WARS GALAXIES gets the proper-noun caps — Michel had a real game he loved, and the joke is that none of these jokers care.
- "DEADMINES" plants the *Michel-as-noob* setup that pays off in Scene 6 ("just gonna look around"). He was a noob from day one. Tobi was always there boosting.
- "One dungeon" is still the punchline-lie.

---

---

## Scene 3 — Bram's living room ("Trains" / Porcupine Tree)

**Setting:** Living room interior, evening. Four sprites scattered around: **Bram, Benny (Bram's brother), Tobi, Michel.** A guitar leaning against the couch.

**Asset notes:** Use `gfx/tilesets/house1.png` (Crystal house interior) palette-swapped warmer. NPC sprites: any 3 distinct ones for Bram/Benny/Tobi. Guitar = custom 8×8 prop sprite.

**Beats:**
- Quiet evening at Bram's place. Just the four of them.
- Michel picks up the guitar, starts playing *Trains* by Porcupine Tree.
- The room goes still.
- Tobi will tell Michel, much later, that this was a very profound moment for him.

**Mechanically:** This is the silent beat. Minimal dialogue — what carries the scene is the *music* (a chiptune motif based on the Trains intro, played on Channel 3 / wave — that's the GBC channel that best fakes a clean guitar) and the *stillness*: no one walks, no one speaks for several beats. After the music ends, one quiet line from Tobi. That's the whole scene.

**Draft dialogue:**

```
[BRAM'S LIVING ROOM.
Evening. Lamp on.]
[Bram on the couch. Benny on
the floor. Tobi in the chair.
Guitar against the wall.]

[Michel-sprite walks in.]

BRAM:     yo

BENNY:    sup

TOBI:     play something

[Michel-sprite walks to the
guitar. Picks it up.]

[Music: TRAINS intro motif.
Wave channel, sparse. Six
bars.]

[The motif resolves.]

TOBI:     ...
          [▼]
          spasti.

[NARRATOR: ▼ Walk on.]
```

**Notes:**
- Trimmed of all the over-explaining. The music does the work; "..." then "spasti." is enough.
- "Spasti" third time. Each use has reframed the word: judgment → peer pressure (absent in Scene 2, evolved) → quiet affection here. The shift happens in *how* Tobi says it, not in any narrator gloss.
- Music: wave-channel arpeggio suggesting the *Trains* intro. Doesn't have to nail the song — has to nail the *feeling*. If we can't, fall back to silence + a single guitar-string SFX.

---

---

## Scene 4 — Spain, "La Cubanita" bar (vacation, ~age 18)

**Setting:** Small bar interior, warm palette. Two waitress NPC sprites behind a counter. Bottles on shelves. Tables. Tobi-sprite and Michel-sprite at a table front-and-center. Tobi gets more wobble-frames as the scene progresses.

**Asset notes:** Use a Crystal cafe/pub tile from `gfx/tilesets/` (look in `mahogany_redgyarados`-area sets, or recolor a `house1` interior). Waitresses = reuse `gfx/sprites/beauty.png` palette-swapped. "Drunk Tobi" = the same NPC sprite with a tilted frame or sweat-drop emote (Pokémon has the canonical `gfx/emotes/` set — perfect).

**Beats:**
- Vacation in Spain. ~18 years old. Just the two of them at the bar (Tobi was there with his family, but the bar runs are him + Michel).
- A bar they keep returning to because the waitresses are cute.
- The waitresses know exactly what's happening and keep bringing more drinks.
- One night Tobi gets *catastrophically* drunk and pukes all over his bed.
- His parents come back from their trip out and find the aftermath. Tobi's dad: not amused.

**Mechanically:** The scene is a tiny loop. Player walks Michel-sprite up to the counter. A waitress prompt: `ANOTHER ROUND?` `YES / NO`. The player picks YES. Tobi's wobble-frame intensifies. Screen does a brief horizon-shake effect on each round. After 3 rounds the screen fades, cut to the bedroom the next morning.

**Draft dialogue:**

```
[LA CUBANITA. Evening.
Music thumping somewhere.]
[Michel-sprite and Tobi-
sprite at a table near the
bar. Two waitresses behind
the counter, smiling.]

TOBI:     ...
          [▼]
          they're definitely
          flirting

MICHEL:   they're definitely
          flirting with our
          WALLETS

TOBI:     no
          [▼]
          no this time it's
          real

MICHEL:   it's never real

TOBI:     spasti

[Player walks Michel-sprite
up to the bar.]

WAITRESS: hola guapo
          [▼]
          ANOTHER ROUND?

> YES
  NO

[YES.]
[Tobi-sprite gets a sweat-
drop emote. Wobble.]

WAITRESS: ...
          [▼]
          ANOTHER ROUND?

> YES
  NO

[YES.]
[Tobi-sprite leans 30°.
Screen does a small shake.]

WAITRESS: ...
          ¿estás seguro?
          [▼]
          ANOTHER ROUND?

> YES
  NO

[YES.]

           * BURP *

[Screen fades to black.]

[CUT TO:
 BEDROOM. MORNING.]
[Tobi-sprite on the bed.
The bed has a "stained"
overlay tile. Tobi-sprite
is fully horizontal.]

TOBI:     ...
          [▼]
          oh no

[A door slam offscreen.]

TOBI'S DAD: (offscreen)
            TOBIAS.
            [▼]
            TOBIAS.
            WHAT.
            HAPPENED.

TOBI:     spasti.

MICHEL:   me?
          [▼]
          you puked on yourself

TOBI:     yeah but you LET me

[NARRATOR: ▼ Walk on.]
```

**Notes:**
- "Spasti" fourth time, now used by both of them and at each other. The word is fully theirs.
- "TOBIAS" (his full name) from his dad off-screen — that universal *parent uses your full name when furious* moment.
- The full bilingual touch ("hola guapo", "¿estás seguro?") in the waitress lines is enough to read as Spain without translating.
- The "you LET me" closer is the kind of victim-blaming joke teenage friends actually make. Reads true.

---

---

## Scene 5 — Aachen, the club stairs (CLIMAX)

**Setting:** Street outside a club in Aachen, at night. Dark palette. Bouncer NPC silhouette by the door. Tobi-sprite alone on the stairs.

**Beats:**
- You both went out clubbing in Aachen.
- Michel notices Tobi has left the club, follows him out.
- Tobi is sitting on the stairs in front of the entrance.
- Michel sits down next to him.
- Tobi tells Michel his mom died that morning. He hasn't told anyone.
- He breaks down. Michel hugs him.
- "I knew I'd love this kid for the rest of my life like a brother."
- A few guys make fun of them for hugging. Michel flips his shit.

**Mechanically:** The whole scene is one fixed camera angle. No walking. Dialogue. The hug is a sprite overlap with a heart pixel (or no overlay at all — the dialogue carries it). The catcalling guys appear, brief confrontation, Michel-sprite turns and the screen flashes or shakes — keep it short, don't undercut the moment with extended combat.

This is the emotional load-bearing scene of the whole game. Every other scene exists to make the player (Tobi) trust the game enough to let this one land.

**Need from user:**
- The name of the club, or "a club in Aachen" if unspecified
- Are you comfortable with the catcalling-guys beat being explicit, or do you want it softer / cut entirely
- A line Michel actually said, or thought, that night — if you remember one

---

## Scene 6 — Blackwing Lair, first raid (comedy beat after the climax)

**Setting:** The Razorgore egg room — a dim cave chamber with dragon eggs in the center, doorways on either side, mobs about to spawn. Tile-art note: we'll fake the BWL aesthetic with a cave palette (use `gfx/tilesets/cave.png` or `gfx/tilesets/dark_cave.png` from pokecrystal, palette-swap to red/black) and a couple of dragon-egg sprites as scenery. Player-Michel sprite, four NPC-raider sprites lined up behind him as a "raid party," a horde of orc-trash sprites just past the doorway.

**Beats:**
- Michel's first raid with Tobi's guild. He has NO idea how anything works.
- The raid is pre-pull, everyone is positioning.
- Michel-sprite drifts forward to look at the eggs.
- Body-pulls all the trash in the egg room. Mobs swarm.
- 40-man wipe.
- Kicked from the raid team. Demoted to the worse team.
- Tobi is dying laughing on Ventrilo / TeamSpeak.

**Mechanically:** This is a tiny anti-puzzle the player *can't win*. On scene enter, a WoW-style zone banner reads **"Blackwing Lair"** centered on the screen. The raid lead **Aronian** tells the player **"DEFINITELY DON'T WALK LEFT OR RIGHT."** That instruction *is* the trap — a Pokémon player given a "do not" will absolutely do it. The moment Michel-sprite walks one tile left or right, trash spawns from that side's doorway. The wipe is scripted; the gag is the explicit anti-instruction.

**Guild roster on Vent:** Aronian (raidlead, takes everything personally), Tobi (heals), and at minimum Gerrit, Tita, Divinity, Friets, Aerendil chiming in. Each gets one line in the post-wipe chaos — every name is a real person Tobi will instantly recognize.

**Draft dialogue (first pass):**

```
[CAVE INTERIOR. Red palette.
 Dragon eggs in the center.]
[Michel-sprite at the front
of a line of NPC raiders.
Tobi-sprite somewhere in
the back, on heals.]

[A banner slides in from the
top of the screen and rests
mid-screen, WoW zone-change
style:]

           ╔══════════════╗
           ║ BLACKWING    ║
           ║    LAIR      ║
           ╚══════════════╝
           < Bound by Blood >

[Banner fades after 2 seconds.
"Bound by Blood" lingers half
a second longer — that's the
guild Michel just joined.]

VENT CHAT:    <Aronian> ok we
              pull in 30 sec
              [▼]
              <Aronian>
              EVERYONE
              [▼]
              <Aronian>
              DEFINITELY DO NOT
              WALK LEFT OR RIGHT
              [▼]
              <Aronian> stay on
              your mark
              [▼]
              <Friets> lmao who
              would do that
              [▼]
              <Tobi> michel u
              hear that
              [▼]
              <Michel> ya all good
              [▼]
              <Michel> just gonna
              look around

[The player has control of
Michel-sprite. North wall =
eggs. East and west = dark
tunnel doorways. Forward
(north) is fine. Left or
right... is not.]

[Player presses ← or →.]

           ! ! !

[Orc trash floods in from
the doorway Michel walked
toward.]

VENT CHAT:    <Gerrit> ADDS
              [▼]
              <Tita> WHERE
              [▼]
              <Divinity> oh no
              [▼]
              <Aerendil> by the
              Light...
              [▼]
              <Friets> LMAOOOO

VENT CHAT:    <Raidlead> WHO
              [▼]
              <Raidlead> WHO
              PULLED
              [▼]
              <Tobi> oh my god
              [▼]
              <Tobi> oh my GOD
              [▼]
              <Raidlead> WIPE IT
              WIPE IT WIPE IT

[Screen flashes red.
"YOU HAVE DIED" text.
Then the rest of the raid.
40-man wipe.]

           * WIPE *

[Black screen.]

VENT CHAT:    <Aronian> ...
              [▼]
              <Aronian> who is
              this guy
              [▼]
              <Tobi> uhhhh
              [▼]
              <Tobi> my friend
              [▼]
              <Gerrit> oof
              [▼]
              <Friets> RIP
              michel
              [▼]
              <Aronian> hes off
              the team
              [▼]
              <Aronian> demoted.
              casual rank.
              [▼]
              <Tita> sorry
              michel :(
              [▼]
              <Aerendil> a noble
              attempt friend
              [▼]
              <Divinity> ...
              [▼]
              <Tobi> michel
              [▼]
              <Tobi> ...
              [▼]
              <Tobi> spasti.
              [▼]
              <Michel> yeah ok
              fair

[Scene fades.
Both of them are laughing
by the end. You can tell.]
```

**Notes on this draft:**
- Vent chat formatted as a chat log inside the dialogue box — `<Name> text` cadence is instantly recognizable to anyone who voice-chatted in 2005.
- The callback to "spasti" from Scene 1 lands here. The first time Tobi said it, he didn't know Michel. The second time, he says it because Michel is family.
- The raidlead's "who is this guy" mirrors Tobi's Scene 1 line. Different room, same question, very different answer.
- Pokémon-style **`! ! !`** alarm (the same one used when a trainer spots you) for the spawn trigger — it's a perfect canonical glyph for "oh no."
- No music during the wipe. Music returns when the screen fades.

**Locked:**
- Guild: **Bound by Blood**
- Demotion: real.

**Still need (optional polish):**
- Year? (BWL was current content roughly 2005–2006 — sets your age.)
- Are the personality reads above (Friets = the LMAO guy, Aerendil = lore-serious, Divinity = quiet "...", Tita = the empath, Gerrit = the curt warrior) right or wrong? Easy to reassign if so.

---

## Scene 7 — Present day / The Ask

**Setting:** TBD. Could be:
  (a) Michel's apartment (player wakes up, "20 years later…")
  (b) A wedding-themed location (church / venue)
  (c) Just a black screen with the question
  (d) Pokémon-credits-style scrolling montage of all the previous scenes' rooms, then the ask

**Beats:**
- The "you've come this far" moment.
- The actual question.
- A choice prompt: `YES` / `NO`. Both branches go to "YES" — but the NO branch should land a joke ("Press A to reconsider.") then accept YES.

**Need from user:**
- The actual ask line, in your voice. Even rough.
- Wedding date / "save the date" — does the game tell him a date?
- Anything you want to give him in-game as a "key item" — like a literal Pokémon-style item received notification: "TOBI received the BEST MAN BADGE!"

---

## Open questions / decisions

1. **Tobi's nickname** — what do you actually call him?
2. **Order of comedy scenes** — keep Spain before the gut-punch (comedy → devastation = strongest contrast), or put Spain after Aachen to land on a lighter note? My instinct: comedy first, then climax, then resolution. The current order.
3. **Should the "Trains" living-room scene have actual chiptune music** of the song, or just silence + an instrument icon? Silence might be more powerful given the constraint.
4. **Length budget** — total game length: 5–10 min walkthrough? Each scene gets ~30–60 seconds of dialogue.
5. **The girlfriend in Meerbusch** — she's set dressing for the dress-shirt joke. Stay anonymous or named?
6. **Other beats not yet placed:**
   - WoW sessions / "hanging out every day"
   - Starting the Japanese bachelor together (Tobi finished, Michel didn't)
   - "Big highs and lows" mentioned generally — is there one more specific high or low we should place?
   - 20 years of friendship leading to now — bridged in scene 6 or earned through a montage

## Asset map (so far)

| Scene | Tileset | Custom art needed |
|---|---|---|
| Classroom | Need school-interior tileset; closest in pret: `interior`, `kanto_pokecenter`-style desks | Tobi NPC sprite, school-uniform Michel |
| Schoolyard | `johto` outdoor tileset + custom gym building? | Friend-group NPC cluster |
| Living room | `house1.png` / `house2.png` interiors | Guitar item icon |
| Spain bar | Custom — closest pret match: any pub/cafe interior in `gfx/tilesets/` | 2× waitress NPC, drunk-Tobi sprite variant |
| Aachen stairs | Custom — could repurpose any night-exterior tile | Hug overlay or paired-sprite frame |
| Present / Ask | Custom — possibly black BG + portrait | Best Man Badge item sprite |

Most of this can reuse pret tilesets with palette swaps. Custom art = mostly Tobi's NPC sprite + the "best man badge."
